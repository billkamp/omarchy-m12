from __future__ import annotations

from pyinfra import host
from pyinfra.api import operation
from pyinfra.api.command import QuoteString, StringCommand
from pyinfra.facts.server import Home

from omarchy_m12.constants import OMARCHY_REMOTE


def _omarchy_checkout() -> str:
    home = host.get_fact(Home)
    if not home:
        raise ValueError("Could not determine target user home directory")
    return f"{home}/.local/share/omarchy"


def _quoted(value: str) -> str:
    return StringCommand(QuoteString(value)).get_raw_value()


def _omarchy_shell(command: str) -> StringCommand:
    checkout = _quoted(_omarchy_checkout())
    script = (
        "set -eo pipefail; "
        "sudo -n true; "
        "while true; do sudo -n true; sleep 60; done 2>/dev/null & "
        "sudo_keepalive_pid=$!; "
        "trap 'kill \"$sudo_keepalive_pid\" 2>/dev/null || true' EXIT; "
        f"export OMARCHY_PATH={checkout}; "
        'export PATH="$OMARCHY_PATH/bin:$PATH"; '
        f"{command}"
    )
    return StringCommand("bash", "-lc", QuoteString(script))


@operation()
def switch_branch(ref: str = "omarchy-shell"):
    """Reset the Omarchy checkout to the requested upstream ref."""

    checkout = _quoted(_omarchy_checkout())
    remote = _quoted(OMARCHY_REMOTE)
    ref_quoted = _quoted(ref)
    remote_ref = _quoted(f"origin/{ref}")

    yield (
        f"cd {checkout} && "
        f"git remote set-url origin {remote} && "
        f"git fetch origin {ref_quoted} && "
        f"git switch -C {ref_quoted} {remote_ref} && "
        f"git branch --set-upstream-to={remote_ref} {ref_quoted} && "
        f"git reset --hard {remote_ref}"
    )


@operation()
def migrate():
    """Run Omarchy migrations."""

    yield _omarchy_shell("timeout 10m omarchy-migrate")


@operation()
def default_browser(browser: str = "zen"):
    """Set Omarchy's default browser when needed."""

    browser_quoted = _quoted(browser)
    yield (
        "current=$(omarchy-default-browser 2>/dev/null || true); "
        f"[ \"$current\" = {browser_quoted} ] || omarchy-default-browser {browser_quoted}"
    )


@operation()
def default_terminal(terminal: str = "kitty"):
    """Set Omarchy's default terminal when needed."""

    terminal_quoted = _quoted(terminal)
    yield (
        "current=$(omarchy-default-terminal 2>/dev/null || true); "
        f"[ \"$current\" = {terminal_quoted} ] || omarchy-default-terminal {terminal_quoted}"
    )


@operation()
def theme(theme: str = "Everforest"):
    """Set Omarchy's current theme when needed."""

    theme_quoted = _quoted(theme)
    yield (
        "current=$(omarchy-theme-current 2>/dev/null || true); "
        f"[ \"$current\" = {theme_quoted} ] || omarchy-theme-set {theme_quoted}"
    )


@operation()
def webapps_remove_all():
    """Remove Omarchy-managed webapps."""

    yield (
        "if grep -q 'Exec=omarchy-launch-webapp\\|Exec=omarchy-webapp-handler' "
        "$HOME/.local/share/applications/*.desktop 2>/dev/null; then "
        "omarchy-webapp-remove-all; "
        "else echo 'No Omarchy web apps found.'; fi"
    )


@operation()
def update():
    """Run Omarchy's update pipeline without the interactive restart prompt."""

    yield _omarchy_shell(
        "{ "
        "omarchy-snapshot create || (($? == 127)); "
        "omarchy-update-keyring; "
        "omarchy-update-available-reset; "
        "omarchy-update-system-pkgs; "
        "omarchy-migrate; "
        "omarchy-update-aur-pkgs; "
        "omarchy-update-mise; "
        "omarchy-update-orphan-pkgs; "
        "omarchy-hook post-update; "
        "omarchy-update-analyze-logs; "
        "} 2>&1 | tee /tmp/omarchy-update.log"
    )
