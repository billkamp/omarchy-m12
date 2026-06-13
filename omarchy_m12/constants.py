from __future__ import annotations

APPLIED_TREE = "~/.local/share/omarchy-m12"
OMARCHY_CHECKOUT = "~/.local/share/omarchy"
YOLK_SOURCE = f"{APPLIED_TREE}/dots"
OMARCHY_REMOTE = "https://github.com/basecamp/omarchy.git"
OMARCHY_REF = "omarchy-shell"
DEFAULT_BROWSER = "zen"
DEFAULT_TERMINAL = "kitty"
DEFAULT_THEME = "Everforest"

OWNED_PACKAGES = (
    "openssh",
    "git",
    "rsync",
    "aur/yolk-bin",
)

RSYNC_EXCLUDE_DIRS = (
    ".git",
    ".venv",
    "__pycache__",
    ".mypy_cache",
    ".ruff_cache",
    ".pytest_cache",
)
