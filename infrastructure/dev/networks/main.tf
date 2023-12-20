resource "google_compute_subnetwork" "subnet" {
  name          = "${var.env}-subnet"
  project       = var.project
  ip_cidr_range = "10.0.0.0/24"
  network       = data.terraform_remote_state.vpc.outputs.vpc_self_link
  region      = var.region
}

resource "google_compute_firewall" "firewall" {
  name    = "${var.env}-${var.project}-firewall-80-443-22"
  project = var.project
  network = data.terraform_remote_state.vpc.outputs.vpc_self_link

  allow {
    protocol = "tcp"
    ports    = ["80", "443", "22"]
  }

  source_ranges = var.ip_public_workers
}