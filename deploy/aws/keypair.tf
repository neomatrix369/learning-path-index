resource "aws_key_pair" "lpi-key" {
  key_name   = "lpi-key"
  public_key = file("~/.ssh/lpi-key.pub")
}