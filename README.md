# omarchy-m12

Host-local Omarchy customization checkout.

## Model

- Editable checkout: `~/src/omarchy-m12`
- Applied tree: `~/.local/share/omarchy-m12`
- Omarchy checkout: `~/.local/share/omarchy`
- Yolk source: `~/.local/share/omarchy-m12/dots`

## Commands

```sh
just bootstrap-ssh
just apply [target]
just upgrade [target]
just doctor [target]
```

The default pyinfra target is `@local`; pass an explicit target to apply, upgrade, or doctor when needed.
`bootstrap-ssh` is not routed through pyinfra; it runs `sudo systemctl enable --now sshd` and `sudo ufw allow OpenSSH` directly.

Phase 1 only provides scaffolding and stubs. Full apply and upgrade behavior lands in later phases.
