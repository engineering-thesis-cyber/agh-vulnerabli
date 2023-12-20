include {
  // searches up the directory tree from the current terragrunt.hcl file 
  // and returns the absolute path to the first terragrunt.hcl
  path = find_in_parent_folders()
}
terraform {
    source = "./main.tf"
}
