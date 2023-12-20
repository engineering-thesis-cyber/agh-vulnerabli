# 
locals{
  is_windows = length(regexall(":", lower(abspath(path.root)))) > 0
  key_transfer_linux = "scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i ../../../gcp_ssh ../../../key.json ubuntu@${google_compute_address.external-ip.address}:~"
  key_transfer_windows = "scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=nul -i ..\\..\\..\\gcp_ssh ..\\..\\..\\key.json ubuntu@${google_compute_address.external-ip.address}:~"
  key_transfer_script = local.is_windows ? local.key_transfer_windows : local.key_transfer_linux
}

resource "time_sleep" "wait_60_seconds" {
  create_duration = "60s"
}
resource "random_password" "vm_python_app_password" {
  length           = 12
  special          = false
}

resource "local_file" "app_password" {
  content  = random_password.vm_python_app_password.result
  filename = "${path.module}/../../../password.txt"
}

resource "google_compute_instance" "ubuntu-instance" {
  name         = "ubuntu-instance"
  machine_type = "e2-medium"
  zone         = var.location
  # depends_on   = [time_sleep.wait_60_seconds] 


  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2004-lts"
    }
  }

  network_interface {
    network    = data.terraform_remote_state.vpc.outputs.vpc_network_name
    subnetwork = data.terraform_remote_state.subnet.outputs.subnet_name
    access_config {
      nat_ip = google_compute_address.external-ip.address
    }
  }

  metadata = {
    startup-script = <<-EOF
    #!/bin/bash
    sudo su
    apt-get update
    apt-get install git -y
    apt-get install python3-pip -y
    apt-get install docker.io -y
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
    apt-get install apt-transport-https ca-certificates gnupg
    apt-get update && apt-get install google-cloud-cli
    apt-get install google-cloud-sdk-gke-gcloud-auth-plugin -y
    apt-get install kubectl -y
    docker pull appsecco/dsvw:latest
    docker pull kollbi/dsvw:1.0.0
    docker pull webgoat/webgoat:latest
    docker pull hackersploit/bwapp-docker:latest
    export KUBECONFIG=~/.kube/config
    gcloud auth activate-service-account --key-file=/home/ubuntu/key.json
    gcloud container clusters get-credentials dev-${var.project}-k8s --location ${var.location} --project ${var.project}
    kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/cloud/deploy.yaml
    git clone ${var.repo_link}
    cd vulnerabli/app
    export SIMPLELOGIN_PASSWORD_ENV=${random_password.vm_python_app_password.result}
    echo ${random_password.vm_python_app_password.result} > /vulnerabli/app/SIMPLELOGIN_PASSWORD
    pip3 install -r requirements.txt
    sudo python3 main.py 2>err.log 1>info.log &
    EOF
    ssh-keys = "${google_compute_project_metadata_item.ssh-key.value}"
  }
}

resource "null_resource" "transfer_key" {
    // change private ssh location to gh variables, also key.json should not be in gh files 
  depends_on = [ time_sleep.wait_60_seconds ]
  provisioner "local-exec" {
    command = "${local.key_transfer_script}"
  }
}

resource "google_compute_address" "external-ip" {
  name = "external-ip"
}

resource "google_compute_project_metadata_item" "ssh-key" {
  key   = "ssh-keys"
  value = "ubuntu:${file("gcp_ssh.pub")}"
}

output "is_windows" {
  value = local.is_windows
}

output "app_password" {
  value = nonsensitive(random_password.vm_python_app_password.result)
}