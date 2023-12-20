import os

from app_config import LAB_MAP
from logger_config import l


def folder_cleanup(directory_path: str):
    files = os.listdir(directory_path)
    file_to_keep = "kustomization.yaml"

    try:
        for file in files:
            if file != file_to_keep:
                file_path = os.path.join(directory_path, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted: {file}")
                else:
                    print(f"Not a file: {file}")
    except Exception as e:
        print(f"folder_cleanup: {e}")

    kustomization_data = (
        "apiVersion: kustomize.config.k8s.io/v1beta1\n"
        "kind: Kustomization\n\n"
        "resources:\n"
    )
    try:
        kustomization = open(f"{directory_path}/kustomization.yaml", "w")
        kustomization.write(kustomization_data)
    except Exception as e:
        l.error(
            f"unable to write template data to kustomization.yaml file in folder_cleanup: {e}"
        )


def setup_yaml_for_deployment(yaml_directory: str, copies: int, id: int):
    folder_cleanup(yaml_directory)
    kustomization_data = (
        "apiVersion: kustomize.config.k8s.io/v1beta1\n"
        "kind: Kustomization\n\n"
        "resources:\n"
    )
    for i in range(copies):
        replacements = {"APP_NAME": f"user{i}", "NUMBER": str(id)}

        try:
            with open(f"./deployments/deployment_lab_{LAB_MAP[id]}.yaml", "r") as f:
                data = f.read()

            for old, new in replacements.items():
                data = data.replace(old, new)

            yaml_file_name = f"lab{id}-{replacements['APP_NAME']}.yaml"
            kustomization_data += "".join(f"- {yaml_file_name}\n")

            deployment_yaml = open(f"{yaml_directory}/{yaml_file_name}", "w")
            deployment_yaml.write(data)
        except Exception as e:
            l.error(f"setup_yaml_for_deployment: {e}")

    try:
        kustomization = open(f"{yaml_directory}/kustomization.yaml", "w")
        kustomization.write(kustomization_data)
    except Exception as e:
        l.error(f"setup_yaml_for_deployment: {e}")
