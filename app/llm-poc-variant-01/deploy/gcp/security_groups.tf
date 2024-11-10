resource "google_compute_firewall" "lpi-sg" {
  name    = "lpi-sg"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["lpi-sg"]
}
