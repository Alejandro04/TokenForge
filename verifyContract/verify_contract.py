#!/usr/bin/env python3
"""
Compute constructor arguments and open Etherscan verification page.
No API key needed — paste the source code manually.

Usage:
    python verify_contract.py
"""

from __future__ import annotations

import os
import sys
import webbrowser
from typing import Any

# Allow running from any directory — ensure project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web3 import Web3

from forge.contracts import ERC20_SOURCE, ERC721_SOURCE

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


def _select(message: str, choices: dict[str, str]) -> str:
    print(f"\n{CYAN}{message}{RESET}")
    keys = list(choices)
    for i, label in enumerate(keys, 1):
        print(f"  {GREEN}[{i}]{RESET} {label}")
    while True:
        try:
            pick = int(input(f"\n  Choice [1-{len(keys)}]: ").strip())
            if 1 <= pick <= len(keys):
                return keys[pick - 1]
        except ValueError:
            pass
        print(f"{RED}  Invalid choice.{RESET}")


def _ask_text(prompt: str, default: str = "") -> str:
    tail = f" [{default}]" if default else ""
    value = input(f"{prompt}{tail}: ").strip()
    return value or default


def _encode_erc20(name: str, symbol: str, decimals: int, initial_supply: int) -> str:
    w3 = Web3()
    types = ["string", "string", "uint8", "uint256"]
    return w3.codec.encode(types, [name, symbol, decimals, initial_supply]).hex()


def _encode_erc721(name: str, symbol: str) -> str:
    w3 = Web3()
    types = ["string", "string"]
    return w3.codec.encode(types, [name, symbol]).hex()


def main() -> None:
    print(f"\n{CYAN}{BOLD}Verify Contract (Etherscan — no API key needed){RESET}\n")

    network = _select("Network:", {
        "sepolia.etherscan.io": "Sepolia Testnet",
    })

    contract_address = _ask_text("Contract address (0x...)")
    standard = _select("Standard:", {
        "ERC-20": "ERC-20 (Fungible)",
        "ERC-721": "ERC-721 (Non-Fungible)",
    })

    if standard == "ERC-20":
        print(f"\n{CYAN}--- Constructor Arguments{RESET}\n")
        name = _ask_text("Token name")
        symbol = _ask_text("Token symbol")
        decimals = int(_ask_text("Decimals", "18"))
        initial_supply = int(_ask_text("Initial supply"))
        encoded_args = _encode_erc20(name, symbol, decimals, initial_supply)
        source = ERC20_SOURCE
        contract_name = "TokenForgeERC20"
    else:
        print(f"\n{CYAN}--- Constructor Arguments{RESET}\n")
        name = _ask_text("Collection name")
        symbol = _ask_text("Collection symbol")
        encoded_args = _encode_erc721(name, symbol)
        source = ERC721_SOURCE
        contract_name = "TokenForgeERC721"

    # Print source code to a temp file for easy copy-paste
    source_file = f"verify_{contract_name}.sol"
    with open(source_file, "w", encoding="utf-8") as f:
        f.write(source)

    print(f"\n{BOLD}{'=' * 56}{RESET}")
    print(f"{GREEN}  Verification data ready{RESET}")
    print(f"{'=' * 56}")
    print(f"\n  {YELLOW}1. Source code{RESET} -> saved to {GREEN}{source_file}{RESET}")
    print(f"\n  {YELLOW}2. Constructor Arguments (ABI-encoded):{RESET}")
    print(f"     {GREEN}{encoded_args}{RESET}")
    print(f"\n  {YELLOW}3. Compiler version:{RESET}  v0.8.20+commit.a1b79de6")
    print(f"\n  {YELLOW}4. License:{RESET}            MIT")
    print(f"\n  {YELLOW}5. Contract name:{RESET}      {contract_name}")
    print(f"\n  {YELLOW}6. Optimization:{RESET}       No")
    print(f"\n  {BOLD}Open verification page?{RESET}")

    # Open browser
    verify_url = f"https://{network}/verifyContract?a={contract_address}"
    print(f"\n  {CYAN}{verify_url}{RESET}")

    if input(f"\n  Open in browser? [Y/n]: ").strip().lower() not in ("n", "no"):
        webbrowser.open(verify_url)
        print(f"  {GREEN}Browser opened.{RESET}")
        print(f"\n  {BOLD}On the page, fill in:{RESET}")
        print(f"    - Compiler:     v0.8.20+commit.a1b79de6")
        print(f"    - License:      MIT")
        print(f"    - Source:       Paste the contents of {source_file}")
        print(f"    - Constructor:  {encoded_args}")
        print(f"    - Optimization: No")

    print()


if __name__ == "__main__":
    main()
