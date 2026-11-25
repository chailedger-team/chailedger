resource "azurerm_subnet" "bastion" {
  name                 = "AzureBastionSubnet"
  resource_group_name  = azurerm_resource_group.chailedger.name
  virtual_network_name = azurerm_virtual_network.chailedger.name
  address_prefixes     = ["10.0.3.0/26"]
}

resource "azurerm_public_ip" "bastion" {
  name                = "chailedger-bastion-pip"
  location            = azurerm_resource_group.chailedger.location
  resource_group_name = azurerm_resource_group.chailedger.name
  allocation_method   = "Static"
  sku                 = "Standard"

  tags = {
    environment = var.environment
    project     = "chailedger"
  }
}

resource "azurerm_bastion_host" "chailedger" {
  name                = "chailedger-bastion"
  location            = azurerm_resource_group.chailedger.location
  resource_group_name = azurerm_resource_group.chailedger.name
  sku                 = "Basic"

  ip_configuration {
    name                 = "bastion-ip-config"
    subnet_id            = azurerm_subnet.bastion.id
    public_ip_address_id = azurerm_public_ip.bastion.id
  }

  tags = {
    environment = var.environment
    project     = "chailedger"
  }
}
