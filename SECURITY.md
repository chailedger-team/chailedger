# Security

This document covers the security scanning that runs as part of our CI pipeline and any findings that came up.

## Scanning tools

We added two security scans to the GitHub Actions workflow. Both run automatically on every pull request.

### Trivy (container image scanning)

Trivy scans the built Docker image for known vulnerabilities in OS packages and application dependencies. We configured it to flag CRITICAL and HIGH severity issues only so the output stays focused on things that actually matter.

### tfsec (Infrastructure as Code scanning)

tfsec analyses the Terraform configuration files for potential security misconfigurations. Things like overly permissive firewall rules, missing encryption settings, or hardcoded credentials. It runs with soft_fail enabled so it reports issues without blocking the pipeline.

## Findings

### Trivy

No critical or high severity vulnerabilities were found in the container image. The base image is `python:3.12-slim` which has a smaller attack surface compared to the full image. We also use a multi-stage build so build-time dependencies do not end up in the final image.

### tfsec

tfsec flagged the following:

| Finding | Severity | How we handled it |
|---|---|---|
| Finding | Severity | How we handled it |
|---|---|---|
| SSH (port 22) open to all sources | HIGH | Fixed. SSH access is now restricted through a configurable CIDR variable (`allowed_ssh_cidr`). In production this would be set to a specific IP range. The default is left open for development convenience but can be locked down in tfvars. |
| App port (5000) open to all sources | MEDIUM | Acknowledged. A production setup would sit behind a load balancer or gateway instead of exposing the app port directly. |
| No disk encryption specified on VM | HIGH | The Standard_LRS disk type does not enable encryption by default. For a production deployment we would switch to a managed disk with encryption at rest. |

These are valid findings for a production environment. For this stage of the project we documented them and noted what the fixes would look like when we move towards a production setup.

## Notes

Security scanning is an ongoing process. As we add more infrastructure and dependencies, new findings may come up and this document will be updated accordingly.
