output "arn" {
  description = "The ARN of the instance"
  value       = try(aws_instance.lpi-vm.arn, "")
}

output "public_dns" {
  description = "This public DNS name assigned to the instance"
  value       = try(aws_instance.lpi-vm.public_dns, "")
}

output "public_ip" {
  description = "This public IP address assigned to the instance"
  value       = try(aws_instance.lpi-vm.public_ip, "")
}

output "private_dns" {
  description = "This private DNS name assigned to the instance"
  value       = try(aws_instance.lpi-vm.private_dns, "")
}

output "private_ip" {
  description = "This private IP address assigned to the instance"
  value       = try(aws_instance.lpi-vm.private_ip, "")
}


# Outputs the id of the subnet you created in the module
#output "subnet_id" {
#  value = try(aws_subnet.this.id, "")
#}

# Outputs the value of the 
# /aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2 parameter.
#output "ami_id" {
#  value = try(data.aws_ssm_parameter.this.value, "")
#}

output "tags_all" {
  description = "A map of tags assigned to the resource"
  value       = try(aws_instance.lpi-vm.tags_all, "")
}
