from __future__ import annotations

from pyinfra import host
from pyinfra.api import operation
from pyinfra.api.command import QuoteString, StringCommand
from pyinfra.facts.server import Home


def _quoted(value: str) -> str:
    return StringCommand(QuoteString(value)).get_raw_value()


@operation()
def apply(dots_dir: str | None = None):
    """Apply Yolk-managed user files."""

    home = host.get_fact(Home)
    if not home:
        raise ValueError("Could not determine target user home directory")

    dots_dir = dots_dir or f"{home}/.local/share/omarchy-m12/dots"
    config_dir = f"{home}/.config/yolk"

    dots = _quoted(dots_dir)
    config = _quoted(config_dir)

    yield (
        "set -e; "
        f"mkdir -p {_quoted(f'{home}/.config')}; "
        f"if [ -e {config} ] && [ ! -L {config} ]; then "
        "echo 'Refusing to replace ~/.config/yolk because it exists and is not a symlink.' >&2; "
        "echo 'Move it aside manually, then rerun just apply or just upgrade.' >&2; "
        "exit 1; "
        "fi; "
        f"if [ -L {config} ] && [ \"$(readlink {config})\" != {dots} ]; then "
        f"ln -sfn {dots} {config}; "
        "fi; "
        f"if [ ! -e {config} ] && [ ! -L {config} ]; then "
        f"ln -s {dots} {config}; "
        "fi; "
        f"cd {config} && yolk sync"
    )
