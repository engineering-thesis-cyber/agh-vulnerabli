resource "google_compute_network" "vpc_network" {
  project                 = var.project
  name                    = "${var.env}-vpc"
  auto_create_subnetworks = false
}