# GKE cluster
resource "google_container_cluster" "primary" {
  name     = "${var.env}-${var.project}-k8s"
  location = var.location
  project  = var.project
  # We can't create a cluster with no node pool defined, but we want to only use
  # separately managed node pools. So we create the smallest possible default
  # node pool and immediately delete it.
  remove_default_node_pool = true
  initial_node_count       = 1

  network            = data.terraform_remote_state.vpc.outputs.vpc_network_name
  subnetwork         = data.terraform_remote_state.subnet.outputs.subnet_name
}

# Separately Managed Node Pool
resource "google_container_node_pool" "primary_nodes" {
  name       = "${google_container_cluster.primary.name}-node-pool"
  location   = var.location
  cluster    = google_container_cluster.primary.name
  node_count = var.gke_num_nodes

  node_config {
    oauth_scopes = [
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
    ]

    labels = {
      env = var.project
    }

    # preemptible  = true
    machine_type = "e2-standard-2"
    disk_size_gb = 64
    disk_type    = "pd-ssd"
    tags         = ["gke-node", "${var.project}-gke"]
    metadata = {
      disable-legacy-endpoints = "true"
    }
  }
}

resource "null_resource" "add_context"{
  depends_on = [google_container_cluster.primary, google_container_node_pool.primary_nodes]

  provisioner "local-exec" {
    command =  <<EOT
gcloud container clusters get-credentials ${google_container_cluster.primary.name} --location ${var.location} --project ${var.project}
      EOT 
  }
}