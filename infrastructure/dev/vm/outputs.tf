output "instance_ip_address" {
  value       = google_compute_address.external-ip.address
  description = "The public IP address of the newly created instance"
}