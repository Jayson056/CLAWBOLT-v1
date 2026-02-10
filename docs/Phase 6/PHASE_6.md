# Phase 6: Deployment & Hardening

## Objectives
- Ensure the system is "always-on" and resilient.
- Automate installation and service management.
- Hardened system integration.

## Key Components
- **Systemd Service**: Continuous monitoring and auto-restart on failure.
- **Environment Management**: Automated venv setup and dependency resolution.
- **GitHub Prep**: Sanitizing logs, secrets, and local paths for distribution.

## Technical Details
- `clawbolt.service` configuration for production-grade reliability.
- Sudoers hardening to minimize the attack surface.
