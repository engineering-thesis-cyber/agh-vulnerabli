import subprocess

from kubernetes import client, config
from logger_config import l
from utils import folder_cleanup, setup_yaml_for_deployment


def create_deployment(yaml_directory, copies, id):
    setup_yaml_for_deployment(yaml_directory, copies, id)
    cmd = ["kubectl", "apply", "-k", yaml_directory]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode == 0:
        status = result.stdout.decode("utf-8")
        return status
    else:
        error = result.stderr.decode("utf-8")
    l.error(f"create_deployment: {error}")


def delete_deployment(deployment_name):
    cmd = ["kubectl", "delete", "deployment", deployment_name]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode == 0:
        status = result.stdout.decode("utf-8")
        return status
    else:
        error = result.stderr.decode("utf-8")
    l.error(f"delete_deployment: {error}")


def delete_all_deployments(yaml_directory):
    cmd = ["kubectl", "delete", "-k", yaml_directory]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode == 0:
        status = result.stdout.decode("utf-8")
        folder_cleanup(yaml_directory)
        return status
    else:
        error = result.stderr.decode("utf-8")
        l.error(f"delete_all_deployments: {error}")


def info_deployment(lab_id):
    # Get latest info about all pods
    config.load_kube_config()
    api = client.CoreV1Api()
    pod_list = api.list_namespaced_pod(namespace="default")

    users = list()
    try:
        # Get only pods from given lab id
        pod_deployment_list = list()
        for pod in pod_list.items:
            if pod.metadata.name.split("-")[0] == str(lab_id):
                pod_deployment_list.append(pod)
        # Check if at least one pod in given lab id
        if pod_deployment_list == []:
            return f"No pods for lab {lab_id}", False

        # Check status of pods
        for pod in pod_list.items:
            if pod.status.phase != "Running":
                return "Pods are being generated. Try again in few seconds.\n", False

        # Get info about pods in given lab id
        _, cluster_ip = get_external_ip_pods_from_ingress(lab_id)
        pods_info = ""
        for pod in pod_deployment_list:
            url = f"{pod.metadata.name.split('-')[0]}-{pod.metadata.name.split('-')[1]}"
            users.append(url)
            if lab_id == 1:
                pods_info += "".join(
                    f'<p>visit: <a href="http://{cluster_ip}/WebGoat">http://{cluster_ip}/WebGoat</a></p>'
                )
            elif lab_id ==3: #Bwapp specific use case -> redirect to root of ingress IP. /install.php needs to be "first contact point" of this app, to properly bootstrap it.
                pods_info += "".join(
                    f'<p>visit: <a href="http://{cluster_ip}/install.php">http://{cluster_ip}/install.php</a></p>'
                )
            else:
                pods_info += "".join(
                    f'<p>visit: <a href="http://{cluster_ip}/{url}">http://{cluster_ip}/{url}</a></p>'
                )

    except Exception as e:
        l.error(f"info_deployment: {e}")

    return pods_info, True, users


def get_external_ip_pods_from_ingress(lab_id):
    # kubectl get svc -n ingress-nginx -o custom-columns=CLUSTER-IP:.spec.clusterIP --field-selector metadata.name=ingress-nginx-controller
    # kubectl get svc -n ingress-nginx -o jsonpath='{.items[0].status.loadBalancer.ingress[0].ip}'
    cmd = [
        "kubectl",
        "get",
        "svc",
        "-n",
        "ingress-nginx",
        "-o",
        "jsonpath='{.items[0].status.loadBalancer.ingress[0].ip}'",
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        status = result.stdout.decode("utf-8")
        external_ip = str(result.stdout.decode("utf-8"))[1:-1]

        return status, external_ip
    else:
        error = result.stderr.decode("utf-8")
        l.error(f"get_external_ip_pods_from_ingress: {error}")


def restart_machine(lab_id, machine_id):
    cmd = [
        "kubectl",
        "rollout",
        "restart",
        "deployment",
        f"{machine_id}-deployment",
    ]
    # Deleting will restart the pod due to the configuration file and replicas=1
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        status = result.stdout.decode("utf-8")
        return status
    else:
        error = result.stderr.decode("utf-8")
        l.error(f"restart_machine: {error}")


def check_status(lab_id):
    # Get latest info about pods
    config.load_kube_config()
    api = client.CoreV1Api()
    pod_list = api.list_namespaced_pod(namespace="default")

    try:
        machines = list()
        for pod in pod_list.items:
            if pod.metadata.name.split("-")[0] == lab_id:
                url = f"{pod.metadata.name.split('-')[0]}-{pod.metadata.name.split('-')[1]}"
                machines.append(url)
        return f"Got all machines for lab {lab_id}", machines
    except Exception as e:
        l.error(f"check_status: {e}")
