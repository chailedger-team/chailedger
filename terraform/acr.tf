resource "azurerm_container_registry" "chailedger" {
  name                = var.acr_name
  resource_group_name = azurerm_resource_group.chailedger.name
  location            = azurerm_resource_group.chailedger.location
  sku                 = "Basic"
  admin_enabled       = true

  tags = {
    environment = var.environment
    project     = "chailedger"
  }
}
