# Phase 1: Scaffolding

Scaffold `omarchy-m12`.

Create a host-local-checkout Omarchy customization repo. Keep this first pass mostly structural.

Files/directories:

```text
.mise.toml
pyproject.toml
justfile
deploy.py
AGENTS.md
README.md

omarchy_m12/
  __init__.py
  constants.py
  actions.py
  facts/
    __init__.py
    yay.py
  operations/
    __init__.py
    yay.py
    sync.py
    omarchy.py
    yolk.py

dots/
  yolk.rhai
```

Core model:

```text
Editable checkout:
  ~/src/omarchy-m12

Applied tree:
  ~/.local/share/omarchy-m12

Omarchy checkout:
  ~/.local/share/omarchy

Yolk source:
  ~/.local/share/omarchy-m12/dots
```

Execution model:

```text
`pyinfra` may target `@local` or a remote host over SSH.
`just` should default target to `@local`, with optional explicit target arg override.
Run `pyinfra` from checkout where `deploy.py` lives.
"current checkout" always means directory `deploy.py` is run from.
Remote deploys must sync that local checkout to target host before apply/upgrade steps continue.
```

Public commands for this pass:

```text
just apply [target]
just upgrade [target]
just doctor [target]
```

Tooling:

```text
mise manages just and uv/Python
uv manages Python dependencies
Pin exact `pyinfra` version in `pyproject.toml`: `pyinfra==3.9.2`.
just provides command UX
pyinfra manages machine state
Yolk manages user files
yay manages packages
```

Docs to use while implementing:

```text
Yolk docs: https://github.com/elkowar/yolk/tree/main/docs/src
pyinfra docs: https://github.com/pyinfra-dev/pyinfra/tree/3.x/docs
mise docs: https://github.com/jdx/mise/tree/main/docs
```

Suggested `justfile` shape:

```just
sync:
  uv sync

apply target="@local": sync
  uv run pyinfra {{target}} deploy.py --data action=apply

upgrade target="@local": sync
  uv run pyinfra {{target}} deploy.py --data action=upgrade

doctor target="@local": sync
  uv run pyinfra {{target}} deploy.py --data action=doctor
```

`deploy.py` should read `action=apply|upgrade|doctor` and call into `omarchy_m12.actions`.

Do not implement full behavior yet in this phase. Add clean stubs and TODOs only.

# Phase 2

Implement core pyinfra operations and wire them into `apply` / `upgrade`.

Implement `yay` fact and operation based on pyinfra’s pacman fact/operation style.

Required API:

```python
yay.packages(...)
```

Behavior:

```text
Use pacman -Q to read installed packages.
Use yay -S --needed --noconfirm for installs.
Use yay -R --noconfirm for removals.
Support present=True/False.
Support upgrade=False/True.
Handle explicit AUR names like aur/mise-bin by installing aur/mise-bin but checking installed package name mise-bin.
Treat extra/foo and core/foo the same way: install requested spec, check installed package name foo.
Assume Omarchy/base image already provides `yay`; no separate `yay` bootstrap path is required in this plan.
```

`yay.packages(...)` truth table:

```text
present=True, upgrade=False  -> ensure package installed; if already installed, no action
present=True, upgrade=True   -> ensure package installed; if already installed, run yay install command with upgrade semantics, not explicit reinstall semantics
present=False, upgrade=False -> ensure package removed
present=False, upgrade=True  -> same as present=False; ignore upgrade flag
```

Initial owned packages only:

```text
openssh
git
rsync
aur/mise-bin
aur/yolk-bin
```

Implement Omarchy operations:

```python
omarchy.switch_branch(ref="omarchy-shell")
omarchy.default_browser(browser="zen")
omarchy.default_terminal(terminal="kitty")
omarchy.theme(theme="Everforest")
omarchy.webapps_remove_all()
omarchy.update()
```

Behavior:

```text
switch_branch:
  cd ~/.local/share/omarchy
  set origin to https://github.com/basecamp/omarchy.git
  fetch origin omarchy-shell
  switch/reset to origin/omarchy-shell
  run omarchy-migrate
  this operation is intentionally destructive to local modifications in ~/.local/share/omarchy

default_browser:
  use omarchy-default-browser
  set to zen only when needed

default_terminal:
  use omarchy-default-terminal
  set to kitty only when needed

theme:
  use omarchy-theme-current / omarchy-theme-set
  set to Everforest only when needed

webapps_remove_all:
  call omarchy-webapp-remove-all
  remove Omarchy-installed webapp launcher entries only
  do not mutate ~/.config/hypr/bindings.lua in this operation
  make it idempotent

update:
  run omarchy-update
```

Implement applied-tree sync:

```python
sync.applied_tree()
```

Defaults:

```text
source: current checkout where deploy.py is run
dest: ~/.local/share/omarchy-m12 on target host
```

Exclude:

```text
.git
.venv
__pycache__
.mypy_cache
.ruff_cache
.pytest_cache
```

Use rsync. For `@local`, use local rsync. For remote targets, use rsync over SSH. Ensure `rsync` is installed via `yay.packages(...)` before `sync.applied_tree()` runs.

Wire actions as they land.

`apply` order:

```text
yay.packages(..., upgrade=False)
sync.applied_tree()
enable/start sshd via pyinfra systemd operation
omarchy.switch_branch(ref="omarchy-shell")
omarchy.default_browser(browser="zen")
omarchy.default_terminal(terminal="kitty")
omarchy.theme(theme="Everforest")
omarchy.webapps_remove_all()
```

`upgrade` order:

```text
yay.packages(..., upgrade=True)
sync.applied_tree()
omarchy.switch_branch(ref="omarchy-shell")
omarchy.update()
enable/start sshd via pyinfra systemd operation
omarchy.default_browser(browser="zen")
omarchy.default_terminal(terminal="kitty")
omarchy.theme(theme="Everforest")
omarchy.webapps_remove_all()
```

`doctor` checks:

```text
Omarchy branch/ref
default browser = zen
default terminal = kitty
theme = Everforest
sshd status
~/.config/yolk symlink target, or "not configured yet" before Phase 3 lands
```

# Phase 3

Add Yolk application and first user config.

Implement:

```python
yolk.apply()
```

Defaults:

```text
dots_dir = ~/.local/share/omarchy-m12/dots
```

Behavior:

```text
Ensure ~/.config/yolk is symlink to ~/.local/share/omarchy-m12/dots.
If ~/.config/yolk exists and is not symlink, fail loudly with clear manual recovery instructions.
Run yolk sync from ~/.config/yolk.
```

Wire both actions to end with:

```python
yolk.apply()
```

Add minimal Yolk dots only.

Bash:

```text
Keep Omarchy’s default ~/.bashrc structure.
Manage only appended bottom block delimited by stable begin/end markers that loads Bash drop-ins.
Drop-ins live under ~/.config/bash/interactive.d.
Create drop-in directory.
Do not add atuin or ble.sh yet.
```

Hyprland:

```text
Add Yolk-managed ~/.config/hypr/looknfeel.lua override.
Set general.layout = "scrolling".
Set scrolling.column_width = 0.97 for one-column feel.
Keep file minimal so Omarchy defaults still provide rest of config.
Also add Yolk-managed ~/.config/hypr/bindings.lua based on Omarchy's default/hypr/plain-bindings.lua.
Copy plain-bindings.lua into repo-managed Yolk config, then treat that copied file as owned by omarchy-m12.
This removes default Omarchy webapp keybinds without editing ~/.local/share/omarchy directly.
Do not edit ~/.local/share/omarchy directly.
```

Do not add ReFrame, atuin, ble.sh, yazi config, or media-room keybinds in this pass.
