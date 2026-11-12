# Terraform - ChaiLedger Infrastructure

This directory contains the Terraform configuration for provisioning the ChaiLedger application infrastructure on Microsoft Azure.

## What gets provisioned

- A resource group to hold everything together
- A virtual network with one subnet
- A network security group that allows SSH (port 22) and app traffic (port 5000)
- A public IP address
- A Linux virtual machine (Ubuntu 22.04) to run the containerised application

## Prerequisites

- An Azure account with an active subscription
- Terraform v1.5 or later installed on your machine
- Azure CLI installed and logged in (`az login`)
- An SSH public key (generate one with `ssh-keygen` if you don't have it, then pass it as the `ssh_public_key` variable)

## How to use

Start by initialising the working directory. This downloads the Azure provider plugin.

```bash
cd terraform
terraform init
```

To preview what will be created without actually creating anything:

```bash
terraform plan
```

To provision the infrastructure:

```bash
terraform apply
```

Terraform will show a summary of resources to be created and ask for confirmation before proceeding.

## Configuration

All environment-specific values are defined as variables in `variables.tf`. You can override defaults by creating a `terraform.tfvars` file (see `terraform.tfvars.example` for reference).

| Variable | Description | Default |
|---|---|---|
| resource_group_name | Name of the Azure resource group | chailedger-rg |
| location | Azure region | southafricanorth |
| vm_size | VM instance size | Standard_B1s |
| admin_username | SSH admin user | chailedgeradmin |
| environment | Deployment environment tag | dev |

## Cleaning up

To tear down all the resources and avoid charges:

```bash
terraform destroy
```
