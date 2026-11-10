resource "azurerm_resource_group" "chailedger" {
  name     = var.resource_group_name
  location = var.location

  tags = {
    environment = var.environment
    project     = "chailedger"
  }
}

resource "azurerm_virtual_network" "chailedger" {
  name                = "chailedger-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.chailedger.location
  resource_group_name = azurerm_resource_group.chailedger.name

  tags = {
    environment = var.environment
  }
}

resource "azurerm_subnet" "chailedger" {
  name                 = "chailedger-subnet"
  resource_group_name  = azurerm_resource_group.chailedger.name
  virtual_network_name = azurerm_virtual_network.chailedger.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_network_security_group" "chailedger" {
  name                = "chailedger-nsg"
  location            = azurerm_resource_group.chailedger.location
  resource_group_name = azurerm_resource_group.chailedger.name

  security_rule {
    name                       = "allow-ssh"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "allow-http"
    priority                   = 200
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "5000"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  tags = {
    environment = var.environment
  }
}

resource "azurerm_subnet_network_security_group_association" "chailedger" {
  subnet_id                 = azurerm_subnet.chailedger.id
  network_security_group_id = azurerm_network_security_group.chailedger.id
}

resource "azurerm_public_ip" "chailedger" {
  name                = "chailedger-pip"
  location            = azurerm_resource_group.chailedger.location
  resource_group_name = azurerm_resource_group.chailedger.name
  allocation_method   = "Static"
  sku                 = "Standard"

  tags = {
    environment = var.environment
  }
}

resource "azurerm_network_interface" "chailedger" {
  name                = "chailedger-nic"
  location            = azurerm_resource_group.chailedger.location
  resource_group_name = azurerm_resource_group.chailedger.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.chailedger.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.chailedger.id
  }

  tags = {
    environment = var.environment
  }
}

resource "azurerm_linux_virtual_machine" "chailedger" {
  name                            = "chailedger-vm"
  resource_group_name             = azurerm_resource_group.chailedger.name
  location                        = azurerm_resource_group.chailedger.location
  size                            = var.vm_size
  admin_username                  = var.admin_username
  disable_password_authentication = true

  network_interface_ids = [
    azurerm_network_interface.chailedger.id
  ]

  admin_ssh_key {
    username   = var.admin_username
    public_key = file("~/.ssh/id_rsa.pub")
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }

  tags = {
    environment = var.environment
    project     = "chailedger"
  }
}
