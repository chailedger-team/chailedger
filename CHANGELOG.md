# Changelog

All notable changes to ChaiLedger are documented here, from the first project setup through to the summative deployment pipeline.

## Formative 1 - Project Planning

This is where everything started. We set up the repository, agreed on how we would work together, and built the application from scratch.

- Created the GitHub repository and project board with task tracking
- Set up branch protection on `main`: pull requests required, at least one review before merging, stale approvals dismissed, status checks must pass
- Defined the problem: tea farmers in Kenya have no way to verify the weight recorded at buying centres, and every kilogram they lose to a wrong reading means less pay at the end of the month
- Built the Flask REST API with four modules: farmers, deliveries, payments and notifications
- Implemented farmer and buying centre registration with automatic farmer numbering (CL-0001, CL-0002) and phone number normalisation to +254 format
- Implemented delivery recording with validation that rejects zero, negative or unreasonably large weights
- Added the confirm and dispute workflow so farmers can agree with a weighing or challenge it on the same day
- Built monthly statements that calculate estimated pay from confirmed kilograms only
- Added simulated SMS receipts so every weighing and dispute generates a notification
- Built the dispute report that ranks clerks and centres by dispute count
- Wrote unit and API tests covering all four modules
- Set up flake8 for linting
- Wrote the README with setup instructions, usage examples and the African context section explaining why this project matters

## Formative 2 - Containerization and CI

This phase was about making the app reproducible and catching problems automatically.

- Created a multi-stage Dockerfile: the builder stage installs packages, the runtime stage copies only what is needed into a clean python:3.12-slim image
- The app runs as a non-root user (`chailedger`) inside the container so a compromised process cannot take over the host
- Added a Docker healthcheck that verifies the app is responding
- Created docker-compose.yml with a private network, persistent volume for the SQLite database, and a seed service for loading sample data
- Added .dockerignore to keep secrets, tests and Git history out of the image
- Built the GitHub Actions CI pipeline with: flake8 linting, pytest across Python 3.10 to 3.13, Docker image build and health verification, and image publishing to GitHub Container Registry
- Set up CI to run on every push and pull request, with concurrency control to cancel outdated runs

## Summative - The Complete DevOps Pipeline

This is the final phase where we brought everything together into an end-to-end deployment pipeline.

### Infrastructure as Code

- Wrote Terraform configuration for Azure resources: resource group, virtual network with three subnets (public, private, database), network security groups, bastion host, application VM and a public IP
- Added Azure Database for PostgreSQL Flexible Server in a dedicated subnet with private DNS, so the database is reachable from the app VM but not from the public internet
- Made SSH access configurable through the `allowed_ssh_cidr` variable so it can be locked to a specific IP range
- All infrastructure is in the `southafricanorth` region, chosen for proximity to our users in Kenya
- Created terraform.tfvars.example documenting all required variables including the new database settings

### Configuration Management

- Created an Ansible playbook that installs Docker and Docker Compose on the target VM, configures UFW firewall rules, hardens SSH (disables root login and password authentication), copies the application files, and starts the ChaiLedger container
- The playbook includes a health check that waits for the app to respond before reporting success

### Security and DevSecOps

- Added Trivy container image scanning to the CI pipeline, now configured to fail the build on CRITICAL and HIGH vulnerabilities
- Added tfsec scanning for Terraform misconfigurations
- Added pip-audit to check Python dependencies against known vulnerability databases
- Documented all scan findings in SECURITY.md with what we did about each one: multi-stage builds to reduce attack surface, non-root container user, configurable SSH access, and accepted risk documentation for findings without available fixes

### Observability

- Separated `/health` (lightweight process check) from `/readiness` (database connectivity check with response time measurement)
- The `/readiness` endpoint returns a 503 status code when the database is unreachable, so a load balancer knows not to send traffic to a broken instance
- Added structured JSON logging so every log line is a searchable object with timestamp, level, logger name and message
- Updated Docker healthcheck in both Dockerfile and docker-compose.yml to use `/readiness` instead of `/health`

### Documentation

- Updated README with an architecture diagram showing the full system from GitHub Actions through Azure to the running app
- Added Cloud Infrastructure section explaining every Terraform resource and why it exists
- Added Observability section documenting the health and readiness endpoints, structured logging and security scanning
- Updated the technology stack, endpoints table and project structure to reflect all summative additions
