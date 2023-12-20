#generate state dynamically
remote_state {
    backend = "gcs"
    config = {
        bucket      = "terraform-state-bucket-agh-eng-v2"
        prefix      = "${path_relative_to_include()}.tfstate"
        location    = "europe-central2-a"
        project     = "eternal-empire-400716" #swap this on new gcp account
    }
    generate = {
        path      = "state.tf"
        if_exists = "overwrite"
    }
}

#dynamically generate gcp.tf file with provider 
generate "gcp" {
  path      = "gcp.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
    terraform {
      required_providers {
        google = {
          source  = "hashicorp/google"
          version = "3.5.0"
        }
      }
    }

    provider "google" {
      project = "eternal-empire-400716"
      region  = "europe-central2"
    }

EOF
}

generate "variables" {
  path      = "variables_common.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF

#GCP Variables

variable "env" {
  type = string
  validation {
    condition     = can(regex("^dev$|^prod$", var.env))
    error_message = "Invalid environment. Allowed values are dev | prod."
  }
  description = "Variable defining current environment. Possible values are: dev/prod"
}      

variable "location" {
  type = string
  default = "europe-central2-a"
  description = "Location variable to define resource place in gcp."
}

variable "project" {
  type = string
  description = "Name of the project."
}

variable "repo_link" {
  type = string
  description = "Link to repository containing the project code."
}

variable "region" {
  type = string
  description = "Region of the project. Example: eu"
}

variable "gke_username" {
  default     = ""
  description = "gke username"
}

variable "gke_password" {
  default     = ""
  description = "gke password"
}

variable "gke_num_nodes" {
  default     = 1
  description = "number of gke nodes"
}

variable "ip_public_workers" {
  default     = 1
  description = "number of gke nodes"
}

EOF
}

terraform {
    extra_arguments "common_vars"{
        commands = get_terraform_commands_that_need_vars()

        required_var_files = [
            find_in_parent_folders("common.tfvars")
        ]
    }
}