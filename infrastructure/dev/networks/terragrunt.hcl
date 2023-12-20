include {
  // searches up the directory tree from the current terragrunt.hcl file 
  // and returns the absolute path to the first terragrunt.hcl
  path = find_in_parent_folders()
}
terraform {
    source = "./main.tf"
}

locals {
  data_paths = read_terragrunt_config(find_in_parent_folders("data_paths.hcl"))
}


generate "data" {
  path = "data.tf"
  if_exists = "skip"

  contents = <<EOF
    data "terraform_remote_state" "vpc" {
      backend = "gcs"

      config = {
        bucket      = "terraform-state-bucket-agh-eng-v2"
        prefix      = "${local.data_paths.locals.statefile_vpc}"

      }
    }
    EOF
}

dependencies {
  paths = ["../vpc"]
}