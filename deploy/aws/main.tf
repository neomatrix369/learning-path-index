resource "aws_instance" "lpi-gpu-vm" {
  ami = "ami-065deacbcaac64cf2" //Ubuntu AMI
  ### https://aws.amazon.com/ec2/instance-types/
  ###### t2.xlarge = CPU based
  ###### g4dn.xlarge = GPU based
  instance_type = "g4dn.xlarge"
  ebs_block_device {
    device_name = "/dev/sda1"
    volume_size = 20
  }

  tags = {
    Name = "LPI Instance (GPU/vm)"
  }

  key_name        = aws_key_pair.lpi-key.key_name
  security_groups = ["lpi-sg"]

  connection {
    type = "ssh"
    ### Important to set this to the correct user, as for AMI Ubuntu/Linux boxes
    ### the default name is 'ubuntu', and NOT 'ec2-user'
    user        = "ubuntu"
    private_key = file("~/.ssh/lpi-key")
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
      "git clone https://github.com/neomatrix369/learning-path-index",
      "cd learning-path-index/app/llm-poc-variant-01/docker"
    ]
  }
}