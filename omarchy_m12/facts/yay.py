from __future__ import annotations

from typing_extensions import override

from pyinfra.api import FactBase
from pyinfra.facts.pacman import PACMAN_REGEX, parse_packages


class YayPackages(FactBase):
    """Returns installed packages using pacman's local database."""

    default = dict

    @override
    def command(self) -> str:
        return "pacman -Q"

    @override
    def requires_command(self, *args: object, **kwargs: object) -> str:
        return "pacman"

    @override
    def process(self, output: list[str]) -> dict[str, set[str]]:
        return parse_packages(PACMAN_REGEX, output)
