resource "aws_instance" "vm_lpi" {
  ami           = "ami-065deacbcaac64cf2" //Ubuntu AMI
  instance_type = "t2.micro"

  tags = {
    Name = "LPI Instance (vm)"
  }

  key_name        = aws_key_pair.lpi-key.key_name
  security_groups = ["lpi-sg"]

  connection {
    type        = "ssh"
    user        = "ec2-user"
    private_key = file("~/.ssh/lpi-key")
    host        = self.public_ip
  }

  provisioner "file" {
    source      = "./setup-python-and-install-app.sh"
    destination = "/home/ec2-user/setup-python-and-install-app.sh"
  }

#  provisioner "remote-exec" {
#    inline = [
#      "chmod +x /home/ec2-user/setup-python-and-install-app.sh",
#      "sudo sh /home/ec2-user/setup-python-and-install-app.sh"
#    ]
#  }
}