from __future__ import annotations

from pyinfra import host

from omarchy_m12 import actions


def _get_action() -> str:
    action = host.data.get("action", "apply")
    if action not in actions.ACTIONS:
        valid_actions = ", ".join(sorted(actions.ACTIONS))
        raise ValueError(f"Unsupported action {action!r}; expected one of: {valid_actions}")
    return action


actions.ACTIONS[_get_action()]()
