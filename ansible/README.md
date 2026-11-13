# ChaiLedger Ansible Deployment

## Overview
Automates configuration of an Ubuntu 22.04 Azure VM and deploys ChaiLedger using Docker Compose.

## Files
- inventory/hosts.ini: Target VM connection details.
- playbook.yml: Server configuration and application deployment.

## Prerequisites
- Ubuntu 22.04 VM provisioned using Terraform.
- Ansible installed on the control machine.
- SSH key-based access to the VM.
- Internet access from the VM.

## Deployment tasks
1. Verifies the target operating system.
2. Installs Docker Engine and Docker Compose.
3. Enables Docker as a system service.
4. Configures UFW firewall rules for SSH and port 5000.
5. Hardens SSH by disabling root login and password authentication.
6. Copies the ChaiLedger application and Docker configuration.
7. Builds and starts the application using Docker Compose.
8. Checks the application health endpoint.

## Validation and deployment
- Syntax check: ansible-playbook -i inventory/hosts.ini playbook.yml --syntax-check
- Connectivity: ansible chailedger -i inventory/hosts.ini -m ping
- Deployment: ansible-playbook -i inventory/hosts.ini playbook.yml

## Security
- SSH public-key authentication is required.
- Root SSH login and password authentication are disabled.
- UFW denies incoming traffic by default.
- Azure Network Security Groups provide an additional firewall layer.
- The Docker container runs as a non-root user.
- Never commit private keys or application secrets.
- Restrict public access to port 5000 where appropriate.

## Note
Connectivity testing and deployment require a provisioned VM, its public IP address, and the corresponding SSH private key.
