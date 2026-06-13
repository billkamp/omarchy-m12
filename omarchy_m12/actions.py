from __future__ import annotations

from collections.abc import Callable

from pyinfra.operations import server, systemd

from omarchy_m12 import constants
from omarchy_m12.operations import omarchy, sync, yay, yolk


def enable_sshd() -> None:
    systemd.service(
        name="Enable and start sshd",
        service="sshd",
        running=True,
        enabled=True,
        _sudo=True,
    )


def apply() -> None:
    yay.packages(
        name="Install owned packages",
        packages=constants.OWNED_PACKAGES,
        upgrade=False,
    )
    sync.applied_tree(name="Sync applied tree")
    enable_sshd()
    omarchy.switch_branch(
        name="Switch Omarchy branch",
        ref=constants.OMARCHY_REF,
    )
    server.shell(name="Refresh pacman databases", commands="pacman -Sy --noconfirm", _sudo=True, _get_pty=True)
    omarchy.migrate(name="Run Omarchy migrations", _get_pty=True)
    omarchy.default_browser(name="Set default browser", browser=constants.DEFAULT_BROWSER)
    omarchy.default_terminal(name="Set default terminal", terminal=constants.DEFAULT_TERMINAL)
    omarchy.theme(name="Set Omarchy theme", theme=constants.DEFAULT_THEME)
    omarchy.webapps_remove_all(name="Remove Omarchy webapps")
    yolk.apply(name="Apply Yolk dots")


def upgrade() -> None:
    sync.applied_tree(name="Sync applied tree")
    omarchy.switch_branch(
        name="Switch Omarchy branch",
        ref=constants.OMARCHY_REF,
    )
    omarchy.update(name="Update Omarchy", _get_pty=True)
    enable_sshd()
    omarchy.default_browser(name="Set default browser", browser=constants.DEFAULT_BROWSER)
    omarchy.default_terminal(name="Set default terminal", terminal=constants.DEFAULT_TERMINAL)
    omarchy.theme(name="Set Omarchy theme", theme=constants.DEFAULT_THEME)
    omarchy.webapps_remove_all(name="Remove Omarchy webapps")
    yolk.apply(name="Apply Yolk dots")


def doctor() -> None:
    ref = constants.OMARCHY_REF
    browser = constants.DEFAULT_BROWSER
    terminal = constants.DEFAULT_TERMINAL
    theme = constants.DEFAULT_THEME

    server.shell(
        name="Check Omarchy ref",
        commands=(
            "cd ~/.local/share/omarchy && "
            f"git fetch origin {ref} && "
            f"test \"$(git rev-parse HEAD)\" = \"$(git rev-parse origin/{ref})\""
        ),
    )
    server.shell(
        name="Check default browser",
        commands=f'test "$(omarchy-default-browser)" = "{browser}"',
    )
    server.shell(
        name="Check default terminal",
        commands=f'test "$(omarchy-default-terminal)" = "{terminal}"',
    )
    server.shell(
        name="Check Omarchy theme",
        commands=f'test "$(omarchy-theme-current)" = "{theme}"',
    )
    server.shell(
        name="Check sshd status",
        commands="systemctl is-enabled --quiet sshd && systemctl is-active --quiet sshd",
    )
    server.shell(
        name="Check Yolk config link",
        commands=(
            'target="$HOME/.local/share/omarchy-m12/dots"; '
            'if [ ! -e "$HOME/.config/yolk" ]; then '
            'echo "~/.config/yolk not configured yet"; '
            'else test "$(readlink "$HOME/.config/yolk")" = "$target"; fi'
        ),
    )


ACTIONS: dict[str, Callable[[], None]] = {
    "apply": apply,
    "upgrade": upgrade,
    "doctor": doctor,
}
