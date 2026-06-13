from __future__ import annotations

from pathlib import Path

from pyinfra import host, state
from pyinfra.api import operation
from pyinfra.api.command import QuoteString, RsyncCommand, StringCommand
from pyinfra.facts.server import Home

from omarchy_m12.constants import RSYNC_EXCLUDE_DIRS


@operation()
def applied_tree(dest: str | None = None):
    """Sync the current checkout to the applied tree on the target host."""

    home = host.get_fact(Home)
    if not home:
        raise ValueError("Could not determine target user home directory")

    dest = dest or f"{home}/.local/share/omarchy-m12"
    src = f"{Path(state.cwd).resolve()}/"
    flags = ["-az", "--delete", *(f"--exclude={exclude}" for exclude in RSYNC_EXCLUDE_DIRS)]

    yield StringCommand("mkdir", "-p", QuoteString(dest))
    yield RsyncCommand(src, f"{dest}/", flags)
