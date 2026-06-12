# omarchy-m12

Host-local Omarchy customization checkout.

## Model

- Editable checkout: `~/src/omarchy-m12`
- Applied tree: `~/.local/share/omarchy-m12`
- Omarchy checkout: `~/.local/share/omarchy`
- Yolk source: `~/.local/share/omarchy-m12/dots`

## Commands

```sh
just apply [target]
just upgrade [target]
just doctor [target]
```

The default target is `@local`. Remote targets are intended to be passed through to `pyinfra`.

Phase 1 only provides scaffolding and stubs. Full apply and upgrade behavior lands in later phases.
