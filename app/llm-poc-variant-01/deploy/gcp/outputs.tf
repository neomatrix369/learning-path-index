output "self_link" {
  description = "The self link of the instance"
  value       = try(google_compute_instance.lpi-cpu-vm.self_link, "")
}

output "network_interface_0_access_config_0_nat_ip" {
  description = "The external IP address assigned to the instance"
  value       = try(google_compute_instance.lpi-cpu-vm.network_interface[0].access_config[0].nat_ip, "")
}

output "network_interface_0_network_ip" {
  description = "The internal IP address assigned to the instance"
  value       = try(google_compute_instance.lpi-cpu-vm.network_interface[0].network_ip, "")
}

output "tags" {
  description = "A map of tags assigned to the resource"
  value       = try(google_compute_instance.lpi-cpu-vm.tags, {})
}
