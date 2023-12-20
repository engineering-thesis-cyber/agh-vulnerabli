
# Quickstart
To successfully run the app, following conditions have to be met.

### 1. SSH Keys
Create a SSH key-pair, then put both keys inside **infrastructure/dev/vm** folder. File names should be: **gcp_ssh and gcp_ssh.pub** for the private and public key accordingly.

### 2.GCP Credentials File
In the GCP console, navigate to **IAM & Admin** then create a new service account. Download the credentials file and put it into **infrastructure/dev/vm** with the name **key.json**

### 3. Populating Variables File

The common.tfvars file is located  inside **infrastructure folder**, make sure all variables are set.

|Name|Type|Description|
|---|---|---|
|**env**|variable|Environment (dev/qa/prod)|
|**location**|variable|Location of cloud resources (e.g.: "europe-central2-b")|
|**project**|variable|Name of GCP project|
|**region**|variable|Region of cloud resources (e.g.: "europe-central2")|
|**repo_link**|variable|Link to Github repository containing project files|
|**ip_public_workers**|variable|List of IP adressess allowed to connect to VM and K8s cluster|

### 4. Installation of GCP SDK
Use the following guide to install Gcloud SDK based on your operating system:
https://cloud.google.com/sdk/docs/install
### 5. GCP Console Configuration
Make sure all of these APIs/modules are enabled in the GCP console: 
- **Compute Engine API**
- **Kubernetes Engine API**
- **Billings**

### 6. Local GCP Configuration
Login into GCP from your terminal
>**gcloud auth application-default login**

### 7. Terragrunt/Terraform Instalation

Install the following packages:
- **tfenv (1.4.0)**
- **terragrunt**

### 8. Terragrunt Initialization
To initialize terragrunt run the following command from **infrastructure/dev** folder:
>**terragrunt init**

### 9. Running The App
Make sure you are in the **infrastructure/dev** folder in your terminal.
To launch the app, use the following commands:
>**terragrunt run-all plan**

>**terragrunt run-all apply**



