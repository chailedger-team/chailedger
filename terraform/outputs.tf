output "resource_group_name" {
  description = "Name of the resource group"
  value       = azurerm_resource_group.chailedger.name
}

output "vm_public_ip" {
  description = "Public IP address of the VM"
  value       = azurerm_public_ip.chailedger.ip_address
}

output "vm_id" {
  description = "ID of the virtual machine"
  value       = azurerm_linux_virtual_machine.chailedger.id
}

output "vnet_name" {
  description = "Name of the virtual network"
  value       = azurerm_virtual_network.chailedger.name
}

output "nsg_id" {
  description = "ID of the network security group"
  value       = azurerm_network_security_group.chailedger.id
}

output "subnet_id" {
  description = "ID of the subnet"
  value       = azurerm_subnet.chailedger.id
}

output "db_server_fqdn" {
  description = "Fully qualified domain name of the PostgreSQL server"
  value       = azurerm_postgresql_flexible_server.chailedger.fqdn
}

output "db_name" {
  description = "Name of the application database"
  value       = azurerm_postgresql_flexible_server_database.chailedger.name
}

output "bastion_host_name" {
  description = "Name of the Bastion host"
  value       = azurerm_bastion_host.chailedger.name
}

output "acr_login_server" {
  description = "Login server URL of the container registry"
  value       = azurerm_container_registry.chailedger.login_server
}

output "acr_admin_username" {
  description = "Admin username for the container registry"
  value       = azurerm_container_registry.chailedger.admin_username
}

output "acr_admin_password" {
  description = "Admin password for the container registry"
  value       = azurerm_container_registry.chailedger.admin_password
  sensitive   = true
}
