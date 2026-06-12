from __future__ import annotations

from collections.abc import Callable


def apply() -> None:
    # TODO: Wire Phase 2 package, sync, systemd, Omarchy, and Yolk operations.
    pass


def upgrade() -> None:
    # TODO: Wire Phase 2 upgrade operations.
    pass


def doctor() -> None:
    # TODO: Add diagnostics once core operations exist.
    pass


ACTIONS: dict[str, Callable[[], None]] = {
    "apply": apply,
    "upgrade": upgrade,
    "doctor": doctor,
}
