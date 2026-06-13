# AGENTS.md

This repo is a host-local checkout for Omarchy M12 customization.

## Guidelines

- Keep Phase 1 structural; do not implement full machine-state behavior yet.
- Use `just bootstrap-ssh`, `just apply`, `just upgrade`, and `just doctor` as the public command surface.
- Keep `just bootstrap-ssh` outside pyinfra; it should enable/start `sshd` and allow the OpenSSH UFW app directly.
- Route deploy behavior through `deploy.py` and `omarchy_m12.actions`.
- Keep pyinfra operations small and idempotent as they are implemented in later phases.
