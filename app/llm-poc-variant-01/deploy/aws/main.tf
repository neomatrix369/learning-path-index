resource "aws_instance" "lpi-cpu-vm" {
  ami = "ami-065deacbcaac64cf2" //Ubuntu AMI
  ### https://aws.amazon.com/ec2/instance-types/
  ###### t2.xlarge = CPU based
  instance_type = "t2.2xlarge"
  ebs_block_device {
    device_name = "/dev/sda1"
    volume_size = 20
  }

  tags = {
    Name = "LPI Instance (CPU/vm)"
  }

  key_name        = aws_key_pair.lpi-key.key_name
  security_groups = ["lpi-sg"]

  connection {
    type = "ssh"
    ### Important to set this to the correct user, as for AMI Ubuntu/Linux boxes
    ### the default name is 'ubuntu', and NOT 'ec2-user'
    user        = "ubuntu"
    private_key = var.ssh_private_key
    password    = ""
    host        = self.public_ip
  }

  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update -y",
      "sudo apt install -y ca-certificates curl gnupg lsb-release",
      "sudo apt-get update -y",
      "curl -fsSL https://get.docker.com -o get-docker.sh",
      "sudo sh get-docker.sh",
      "sudo groupadd -f docker",
      "sudo usermod -aG docker $USER",
      "docker -v || true",
      "curl https://ollama.ai/install.sh | sh",
      "ollama serve",
      "ollama pull llama2-uncensored",
      "echo; ollama list; echo",
      "git clone https://github.com/neomatrix369/learning-path-index",
      "cd learning-path-index/app/llm-poc-variant-01/",
      "mkdir -p source_documents",
      "curl https://raw.githubusercontent.com/neomatrix369/learning-path-index/main/data/Learning_Pathway_Index.csv -o 'source_documents/Learning Pathway Index.csv'"
    ]
  }
}