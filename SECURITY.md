# Security

This document records the security scans in our GitHub Actions CI pipeline and the findings identified during development.

## Scanning tools

All three scans run automatically through the CI workflow on pull requests targeting main.

### Trivy - container image scanning

Trivy scans the built Docker image for known vulnerabilities in OS packages and application dependencies. It reports HIGH and CRITICAL severity findings.

### tfsec - Infrastructure as Code scanning

tfsec analyses Terraform configuration for security misconfigurations, including network exposure and encryption settings. It runs with soft_fail enabled so findings are reported without blocking the pipeline.

### pip-audit - Python dependency scanning

pip-audit checks the Python dependencies listed in requirements-dev.txt against known vulnerability databases.

## Findings

### Trivy

The latest reported scan found 47 HIGH and 0 CRITICAL vulnerabilities. These findings are documented for review and require ongoing monitoring and remediation. The project uses a multi-stage Docker build and the python:3.12-slim base image to reduce the final image size and attack surface; these measures do not mean all reported vulnerabilities are resolved.

### tfsec

| Finding | Severity | How we handled it |
|---|---|---|
| SSH (port 22) open to all sources by default | HIGH | Added the configurable allowed_ssh_cidr variable so SSH access can be restricted to a trusted IP range. The current default remains 0.0.0.0/0 and should be changed for deployment. |
| App port (5000) open to all sources | MEDIUM | Documented. A production deployment should restrict access or place the application behind a load balancer or gateway. |

### pip-audit

The local dependency audit completed successfully with no known vulnerabilities found in the dependencies listed in requirements-dev.txt.

## Ongoing security

Security findings should be reviewed and remediated as the application and infrastructure evolve. Never commit private keys, credentials, or application secrets.
