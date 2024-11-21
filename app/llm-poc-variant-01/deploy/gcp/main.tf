resource "google_compute_instance" "lpi-cpu-vm" {
  name         = "lpi-llm-cpu"
  machine_type = "n2-standard-8"
  zone         = "europe-west1-b"

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2404-lts-amd64"
      size  = 30
    }
  }

  network_interface {
    network = "default"

    access_config {
      // Include this section to give the VM an external IP address
    }
  }

  metadata_startup_script = <<-EOF
    sudo apt-get update -y
    sudo apt install -y ca-certificates curl gnupg lsb-release
    sudo apt-get update -y

    sudo apt install python3-pip python3.12-venv -y

    # Install Docker
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo groupadd -f docker
    sudo usermod -aG docker $USER
    docker -v || true

    # Install Ollama
    curl https://ollama.ai/install.sh | sh

    # Add a startup service for Ollama
    sudo useradd -r -s /bin/false -U -m -d /usr/share/ollama ollama
    sudo usermod -a -G ollama $(whoami)
    cp ollama.service /etc/systemd/system/ollama.service
    sudo systemctl daemon-reload
    sudo systemctl enable ollama

    sudo systemctl start ollama
    sudo systemctl status ollama

    ollama pull gemma:2b

    sudo git clone https://github.com/neomatrix369/learning-path-index /learning-path-index
    sudo chmod ugo+rwx /learning-path-index
    git config --global --add safe.directory /learning-path-index
    cd /learning-path-index/app/llm-poc-variant-01/
    git checkout gcp-terraform-deploy

    mkdir -p source_documents
    curl https://raw.githubusercontent.com/neomatrix369/learning-path-index/main/data/Learning_Pathway_Index.csv -o 'source_documents/Learning Pathway Index.csv'

    python3 -m venv venv
    . venv/bin/activate
    python3 -m pip install -r requirements.txt

    chainlit run chainlit_app.py --host 0.0.0.0 --port 8000
    EOF

  tags = [
    "lpi-sg",
    "http-server",
    "https-server"
  ]
}
