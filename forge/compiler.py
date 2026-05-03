"""
Solidity compilation wrapper.

Uses py-solc-x to download the solc binary and compile inline sources.
"""

import solcx  # type: ignore[import-untyped]

from forge.contracts import ERC20_SOURCE, ERC721_SOURCE

SOLC_VERSION = "0.8.20"


def _ensure_solc() -> None:
    """Install the solc binary if not already present."""
    if SOLC_VERSION not in solcx.get_installed_solc_versions():
        solcx.install_solc(SOLC_VERSION)


def compile_erc20() -> tuple[list, str]:
    """Return (abi, bytecode) for the ERC-20 contract."""
    _ensure_solc()
    compiled = solcx.compile_source(ERC20_SOURCE, solc_version=SOLC_VERSION)
    interface = compiled["<stdin>:TokenForgeERC20"]
    return interface["abi"], interface["bin"]


def compile_erc721() -> tuple[list, str]:
    """Return (abi, bytecode) for the ERC-721 contract."""
    _ensure_solc()
    compiled = solcx.compile_source(ERC721_SOURCE, solc_version=SOLC_VERSION)
    interface = compiled["<stdin>:TokenForgeERC721"]
    return interface["abi"], interface["bin"]
