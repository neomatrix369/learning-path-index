resource "google_compute_instance" "lpi-cpu-vm" {
  name         = "lpi-cpu-vm"
  machine_type = "n2-standard-8"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2004-lts"
      size  = 20
    }
  }

  network_interface {
    network = "default"

    access_config {
      // Include this section to give the VM an external IP address
    }
  }

  metadata = {
    ssh-keys = "ubuntu:${file("~/.ssh/id_rsa.pub")}"
  }

  tags = ["lpi-sg"]

  metadata_startup_script = <<-EOF
    #!/bin/bash
    sudo apt-get update -y
    sudo apt install -y ca-certificates curl gnupg lsb-release
    sudo apt-get update -y
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo groupadd -f docker
    sudo usermod -aG docker $USER
    docker -v || true
    curl https://ollama.ai/install.sh | sh
    ollama serve
    ollama pull llama2-uncensored
    echo; ollama list; echo
    git clone https://github.com/neomatrix369/learning-path-index
    cd learning-path-index/app/llm-poc-variant-01/
    mkdir -p source_documents
    curl https://raw.githubusercontent.com/neomatrix369/learning-path-index/main/data/Learning_Pathway_Index.csv -o 'source_documents/Learning Pathway Index.csv'
  EOF

  service_account {
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
  }
}
