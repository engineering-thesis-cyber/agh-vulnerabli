# GCP Enable:
- Update project name in /infrastructure/dev/terragrunt.hcl and in common.tfvars!
- Compute Engine API
- Kubernetes Engine API
- Enable Billings
- gcloud auth login (SELECT ACCOUNT UNDER GMAIL DOMAIN!)
- have gcp_ssh & gcp_ssh.pub in infra/vm
- have key.json (From discord) inside infra/dev
- cd infra/dev
- terragrunt run-all apply
- go to gcp (gke) and click connect, and paste the command (like this: gcloud container clusters get-credentials dev-eternal-empire-400716-k8s --zone europe-central2-b --project eternal-empire-400716)

# Base configuration

Get this key:https://console.cloud.google.com/iam-admin/serviceaccounts/details/114835059072579333165/keys?project=inzynierka-agh
Place this key (key.json) inside dev/key.json
gcloud auth application-default login -> auth to terraform via google
install:

- tfenv (1.4.0)
- terragrunt

gcloud container clusters get-credentials dev-eternal-empire-400716-k8s --region europe-central2-a --project eternal-empire-400716

To create new module (folder) make sure it has following files in it:

- At least one .tf file (main.tf) or whatever with terraform code.
- terragrunt.hcl - mandatory!

# Terragrunt.hcl snippet:

```
include {
  // searches up the directory tree from the current terragrunt.hcl file
  // and returns the absolute path to the first terragrunt.hcl
  path = find_in_parent_folders()
}

terraform {
    source = "./main.tf" # point to at least one .tf file
}

locals {
  data_paths = read_terragrunt_config(find_in_parent_folders("data_paths.hcl")) #Required to add data_paths
}

dependencies {
  paths = ["../vpc","../networks"] -> Create this as list, if your module depends on data from another folder, add it there.
}

# data block, make sure to point to proper local in config.prefix -> local.data_paths.locals.statefile_subnet
generate "data" {
  path = "data.tf"
  if_exists = "skip"

  contents = <<EOF
    data "terraform_remote_state" "subnet" {
      backend = "gcs"

      config = {
        bucket      = "terraform-state-bucket-agh"
        prefix      = "${local.data_paths.locals.statefile_subnet}"

      }
    }
    EOF
}

```

# Terragrunt commands:

Same as terraform, examples:
terragrunt apply
terragrunt plan
terragrunt init
terragrunt destroy
terragrunt run-all apply (Make sure to run this inside /dev/infrastructure to run everything in order)

# What to do if remote state cant be reached and gcp throws 403 Account billing in not good state error

Terraform is not using the credentials you get when you run gcloud auth login.
What it uses are the credentials being generated when you run gcloud auth application-default login
it also sets a billing quota project here according to what you have set under core/project.
