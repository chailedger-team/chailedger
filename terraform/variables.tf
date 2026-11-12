variable "resource_group_name" {
  description = "Name of the Azure resource group"
  type        = string
  default     = "chailedger-rg"
}

variable "location" {
  description = "Azure region to deploy resources"
  type        = string
  default     = "southafricanorth"
}

variable "vm_size" {
  description = "Size of the virtual machine"
  type        = string
  default     = "Standard_B1s"
}

variable "admin_username" {
  description = "Admin username for the VM"
  type        = string
  default     = "chailedgeradmin"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}

variable "ssh_public_key" {
  description = "SSH public key for VM access"
  type        = string
}
