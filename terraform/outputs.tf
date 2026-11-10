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
