from __future__ import annotations

from collections.abc import Iterable

from pyinfra import host
from pyinfra.api import operation
from pyinfra.api.command import QuoteString, StringCommand

from omarchy_m12.facts.yay import YayPackages


def _as_list(packages: str | Iterable[str] | None) -> list[str]:
    if packages is None:
        return []
    if isinstance(packages, str):
        return [packages]
    return list(packages)


def _installed_name(package: str) -> str:
    return package.rsplit("/", 1)[-1]


def _quoted_join(packages: list[str]) -> str:
    return " ".join(StringCommand(QuoteString(package)).get_raw_value() for package in packages)


YAY_INSTALL_COMMAND = (
    "yay -S --needed --noconfirm "
    "--answerclean None --answerdiff None --answeredit None --answerupgrade None "
    "--removemake"
)


@operation()
def packages(
    packages: str | Iterable[str] | None = None,
    present: bool = True,
    upgrade: bool = False,
):
    """Install, upgrade, or remove packages with yay."""

    requested_packages = _as_list(packages)
    if not requested_packages:
        return

    installed_packages = host.get_fact(YayPackages)

    if present:
        if upgrade:
            yield f"{YAY_INSTALL_COMMAND} {_quoted_join(requested_packages)}"
            return

        missing_packages = [
            package
            for package in requested_packages
            if _installed_name(package) not in installed_packages
        ]

        for package in requested_packages:
            name = _installed_name(package)
            if name in installed_packages:
                host.noop(f"package {name} is installed")

        if missing_packages:
            yield f"{YAY_INSTALL_COMMAND} {_quoted_join(missing_packages)}"
        return

    installed_requested_packages = [
        _installed_name(package)
        for package in requested_packages
        if _installed_name(package) in installed_packages
    ]

    for package in requested_packages:
        name = _installed_name(package)
        if name not in installed_packages:
            host.noop(f"package {name} is not installed")

    if installed_requested_packages:
        yield f"yay -R --noconfirm {_quoted_join(installed_requested_packages)}"
