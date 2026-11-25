# Security

This document records the security scans in our GitHub Actions CI pipeline and the findings we identified during development. It also tracks what we did about each finding.

## Scanning tools

All three scans run automatically through the CI workflow on pull requests targeting main.

### Trivy (container image scanning)

Trivy scans the built Docker image for known vulnerabilities in OS packages and application dependencies. It reports HIGH and CRITICAL severity findings. As of the summative phase, the pipeline is configured to fail the build if any CRITICAL or HIGH vulnerability is detected. This means no image with a known critical flaw can be merged into main without someone deliberately addressing the finding first.

### tfsec (Infrastructure as Code scanning)

tfsec analyses Terraform configuration for security misconfigurations, including network exposure and encryption settings. It currently runs with soft_fail enabled so findings are reported without blocking the pipeline. Removing soft_fail and enforcing a strict pass is planned so that insecure infrastructure changes are caught before they reach production.

### pip-audit (Python dependency scanning)

pip-audit checks the Python dependencies listed in requirements-dev.txt against known vulnerability databases.

## Findings and remediation

### Trivy findings

The latest scan found 47 HIGH and 0 CRITICAL vulnerabilities in the python:3.12-slim base image. Most of these come from OS-level packages shipped with Debian, not from our own code or Python dependencies.

**What we did about it:**

- We use a multi-stage Docker build so that build tools and their vulnerabilities never reach the final image. Only the slim runtime and our installed packages are copied over.
- The app runs as a non-root user called `chailedger` inside the container. Even if an attacker exploited one of these OS vulnerabilities, they would not have root access to do further damage.
- We configured Trivy to fail the build on CRITICAL and HIGH findings (exit-code set to 1 in ci.yml). This was not the case before. Previously, Trivy would print the report and the pipeline would continue regardless. Now the team must review and address findings before merging.
- The 47 HIGH findings are inherited from the Debian base layer and do not have upstream fixes available yet. We accept this risk for now because downgrading to an alpine base would require rewriting parts of the Docker setup and testing compatibility. We will revisit when the next python slim release ships with patches.

### tfsec findings

| Finding | Severity | Status | What we did |
|---|---|---|---|
| SSH (port 22) open to all sources by default | HIGH | Mitigated | Added the `allowed_ssh_cidr` variable so SSH access can be locked to a specific IP range instead of the whole internet. The default is still 0.0.0.0/0 in the example file, but production deployments must set this to the team's actual IP. |
| App port (5000) open to all sources | MEDIUM | Accepted risk | For a student project, the app needs to be reachable for the demo. In a real production setup, this would sit behind a load balancer or API gateway that handles TLS termination and rate limiting. Documented as accepted risk. |

### pip-audit findings

The dependency audit completed with no known vulnerabilities found. This is checked on every CI run so new vulnerabilities in our Python packages would be caught as soon as they are published.

## Security practices

- Private keys, credentials, and application secrets are never committed to the repository. All sensitive values are passed through environment variables or GitHub Secrets.
- The .env file is listed in .gitignore and .dockerignore so it cannot accidentally end up in a commit or inside the Docker image.
- Branch protection on main requires at least one approving review before merging, so no single person can push unreviewed code into production.
