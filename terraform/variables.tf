variable "resource_group_name" {
  description = "Name of the Azure resource group"
  type        = string
  default     = "chailedger-rg"
}

variable "location" {
  description = "Azure region to deploy resources"
  type        = string
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

variable "allowed_ssh_cidr" {
  description = "CIDR block allowed to SSH into the VM"
  type        = string
  default     = "0.0.0.0/0"
}

variable "db_server_name" {
  description = "Name of the PostgreSQL flexible server"
  type        = string
  default     = "chailedger-db"
}

variable "db_admin_username" {
  description = "Admin username for the PostgreSQL server"
  type        = string
  default     = "chailedgeradmin"
}

variable "db_admin_password" {
  description = "Admin password for the PostgreSQL server"
  type        = string
  sensitive   = true
}

variable "db_sku_name" {
  description = "SKU for the PostgreSQL flexible server"
  type        = string
  default     = "B_Standard_B1ms"
}
