<h3 align="center">🛠️ infra-upgrade</h3>

<div align="center">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/language-unknown-lightgrey.svg" alt="Language: unknown">
  <img src="https://img.shields.io/badge/build-pending-lightgrey.svg" alt="Build: pending">
  <img src="https://img.shields.io/badge/stars-0-lightgrey.svg" alt="Stars: 0">
</div>

---

# 🚀 infra-upgrade

**Power DevOps teams with automated infrastructure upgrades.**  
A lightweight CLI that scans your cloud infra, generates upgrade plans, and applies them with minimal downtime.

## Why infra‑upgrade?

- **Rapid compliance** – automatically detect and remediate infra drift in < 5 min.  
- **Zero‑downtime** – roll‑out upgrades with blue‑green or canary strategies.  
- **Audit‑ready** – generate signed change logs for SOC‑2, ISO 27001, etc.  
- **Built for** – cloud‑native teams using Terraform, Pulumi, or CloudFormation.  
- **Cost‑effective** – reduce manual effort by 70 % and avoid costly rollback incidents.  
- **Open‑source** – community‑driven plugins for AWS, GCP, Azure, and Kubernetes.  

## Feature Overview

| Feature | Description |
|---------|-------------|
| **Infrastructure Discovery** | Auto‑detects resources across multiple clouds and IaC tools. |
| **Upgrade Planner** | Generates a safe, ordered upgrade plan with rollback points. |
| **Canary & Blue‑Green Deploys** | Supports zero‑downtime upgrades for Kubernetes, ECS, and GKE. |
| **Audit Trail** | Produces signed, immutable logs of every change. |
| **Plugin Architecture** | Extendable adapters for new cloud providers and IaC tools. |
| **CLI & REST API** | Operate locally or integrate into CI/CD pipelines. |

## Tech Stack

* (To be filled from `decisions/tech-stack.md` once locked)

## Project Structure

```
infra-upgrade/
├── cmd/          # CLI entry points
├── internal/     # Core logic and adapters
├── pkg/          # Reusable libraries
├── plugins/      # Cloud provider plugins
├── scripts/      # Helper scripts
├── test/         # Automated tests
└── README.md
```

## Getting Started

```bash
# Clone the repository
git clone https://github.com/axentx/infra-upgrade.git
cd infra-upgrade

# Build the CLI
make build

# Run the upgrade planner
infra-upgrade plan --config infra.yaml

# Apply the upgrade
infra-upgrade apply --plan plan.json
```

## Deploy

```bash
# Deploy the CLI as a Docker container
docker build -t axentx/infra-upgrade:latest .
docker run -it --rm axentx/infra-upgrade:latest plan --config infra.yaml
```

## Status

🚧 **Under development** – Initial commit 45b06dc.  
Recent commit: *Initial commit* – set up project skeleton.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT © Axentx