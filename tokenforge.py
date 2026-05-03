#!/usr/bin/env python3
"""
TokenForge — Open Source Blockchain Asset Tokenizer
====================================================
Interactive CLI wizard to deploy ERC-20 and ERC-721 tokens
on any EVM-compatible blockchain.

Usage
-----
    python tokenforge.py          # interactive wizard
"""

from __future__ import annotations

import sys
from typing import Any

from forge import __version__
from forge.deployer import deploy_erc20, deploy_erc721

# ── ANSI colours ──────────────────────────────────────────────────────────

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

# ── Networks ──────────────────────────────────────────────────────────────

NETWORKS = {
    "Sepolia Testnet": {
        "rpc": "https://rpc.sepolia.org",
        "chain_id": 11155111,
        "explorer": "https://sepolia.etherscan.io",
    },
    "Amoy Testnet (Polygon)": {
        "rpc": "https://rpc-amoy.polygon.technology",
        "chain_id": 80002,
        "explorer": "https://amoy.polygonscan.com",
    },
    "Ethereum Mainnet": {
        "rpc": "https://eth.llamarpc.com",
        "chain_id": 1,
        "explorer": "https://etherscan.io",
    },
    "Polygon Mainnet": {
        "rpc": "https://polygon-rpc.com",
        "chain_id": 137,
        "explorer": "https://polygonscan.com",
    },
    "Arbitrum One": {
        "rpc": "https://arb1.arbitrum.io/rpc",
        "chain_id": 42161,
        "explorer": "https://arbiscan.io",
    },
    "Base": {
        "rpc": "https://mainnet.base.org",
        "chain_id": 8453,
        "explorer": "https://basescan.org",
    },
    "Custom": {},
}

# ── Prompt helpers ────────────────────────────────────────────────────────

# Detect whether we have a real interactive console
try:
    import questionary
    from prompt_toolkit.output.win32 import NoConsoleScreenBufferError

    _STYLE = questionary.Style(
        [
            ("qmark", "fg:#00d2ff bold"),
            ("question", "fg:#ffffff bold"),
            ("answer", "fg:#00d2ff bold"),
            ("pointer", "fg:#00d2ff bold"),
            ("highlighted", "fg:#00d2ff bold"),
            ("selected", "fg:#00ffaa"),
        ]
    )

    # Verify console actually works
    try:
        questionary.text("").unsafe_ask()
        _HAS_QUESTIONARY = True
    except NoConsoleScreenBufferError:
        _HAS_QUESTIONARY = False
except Exception:
    _HAS_QUESTIONARY = False


def _select(message: str, choices: dict[str, str]) -> str:
    """Show a numbered menu and return the chosen key."""
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


def _ask_text(prompt: str, default: str = "", *, password: bool = False) -> str:
    """Ask for a single text value."""
    tail = f" [{default}]" if default else ""
    if password:
        return input(f"{prompt}{tail}: ").strip()
    while True:
        value = input(f"{prompt}{tail}: ").strip()
        if value:
            return value
        if default:
            return default
        print(f"{RED}  This field is required.{RESET}")


def _ask_int(prompt: str, default: str = "") -> int:
    """Ask for an integer value."""
    while True:
        raw = _ask_text(prompt, default)
        try:
            return int(raw)
        except ValueError:
            print(f"{RED}  Must be a number.{RESET}")


def _confirm(prompt: str, default: bool = True) -> bool:
    """Yes / No prompt."""
    yn = "Y/n" if default else "y/N"
    raw = input(f"\n{prompt} [{yn}]: ").strip().lower()
    if raw == "":
        return default
    return raw in ("y", "yes")


# ── Banner ────────────────────────────────────────────────────────────────


def _print_banner() -> None:
    print()
    print(f"{CYAN}{BOLD}")
    print("   _______    _             _______                     ")
    print("  |__   __|  | |           |__   __|                    ")
    print("     | | ___ | | _____ _ __   | | ___  _ __ __ _  ___   ")
    print("     | |/ _ \\| |/ / _ \\ '_ \\  | |/ _ \\| '__/ _` |/ _ \\ ")
    print("     | | (_) |   <  __/ | | | | | (_) | | | (_| |  __/ ")
    print("     |_|\\___/|_|\\_\\___|_| |_| |_|\\___/|_|  \\__, |\\___|")
    print("                                             __/ |      ")
    print("                                            |___/       ")
    print(f"{RESET}")
    print(f"{CYAN}      Tokenize Real-World Assets -- Open Source{RESET}")
    print(f"      {YELLOW}v{__version__}{RESET}")
    print()


# ── Flow steps ────────────────────────────────────────────────────────────


def _choose_network() -> dict[str, Any]:
    if _HAS_QUESTIONARY:
        choice = questionary.select(
            "Select network:",
            choices=[questionary.Choice(title=n, value=n) for n in NETWORKS],
            style=_STYLE,
        ).unsafe_ask()
    else:
        choice = _select("Select network:", {n: n for n in NETWORKS})

    if choice == "Custom":
        rpc = _ask_text("RPC URL")
        explorer = _ask_text("Block explorer URL (optional)")
        return {"rpc": rpc, "chain_id": 0, "explorer": explorer, "name": "Custom"}

    network = NETWORKS[choice].copy()
    network["name"] = choice
    print(f"{GREEN}[OK]{RESET} {choice}")
    return network


def _choose_standard() -> str:
    if _HAS_QUESTIONARY:
        return questionary.select(
            "Token standard:",
            choices=[
                questionary.Choice(
                    title="ERC-20  --  Fungible Token (currency, shares, commodities)",
                    value="ERC-20",
                ),
                questionary.Choice(
                    title="ERC-721 --  Non-Fungible Token (unique assets, real estate, art)",
                    value="ERC-721",
                ),
            ],
            style=_STYLE,
        ).unsafe_ask()
    return _select(
        "Token standard:",
        {
            "ERC-20": "ERC-20  -- Fungible Token (currency, shares, commodities)",
            "ERC-721": "ERC-721 -- Non-Fungible Token (unique assets, real estate, art)",
        },
    )


def _ask_erc20_params() -> dict[str, Any]:
    print(f"\n{CYAN}--- ERC-20 Token Parameters{RESET}\n")
    name = _ask_text("Token name (e.g. TokenForge Gold)")
    symbol = _ask_text("Token symbol (e.g. TFG)")
    decimals = _ask_int("Decimals", default="18")
    initial_supply = _ask_int("Initial supply (in whole tokens, e.g. 1000000)")
    return {"name": name, "symbol": symbol, "decimals": decimals, "initial_supply": initial_supply}


def _ask_erc721_params() -> dict[str, Any]:
    print(f"\n{CYAN}--- ERC-721 Token Parameters{RESET}\n")
    name = _ask_text("Collection name (e.g. TokenForge Art)")
    symbol = _ask_text("Collection symbol (e.g. TFA)")
    return {"name": name, "symbol": symbol}


def _ask_private_key() -> str:
    print(f"\n{YELLOW}{BOLD}!!! SECURITY WARNING{RESET}")
    print(
        f"{YELLOW}"
        "   Never share your private key. For mainnet deployments, use a\n"
        "   dedicated burner wallet with only the funds needed for gas.\n"
        f"{RESET}"
    )
    if _HAS_QUESTIONARY:
        return questionary.password(
            "Private key (0x...):",
            validate=lambda s: (s.startswith("0x") and len(s) == 66)
            or "Must be a 64-char hex key prefixed with 0x",
            style=_STYLE,
        ).unsafe_ask()
    return _ask_text("Private key (0x...)", password=True)


def _confirm_and_deploy(
    *,
    network: dict[str, Any],
    standard: str,
    params: dict[str, Any],
    private_key: str,
) -> None:
    print(f"\n{'=' * 56}")
    print(f"{CYAN}  Deployment Summary{RESET}")
    print(f"{'=' * 56}")
    print(f"  Network  : {network['name']}")
    print(f"  RPC      : {network['rpc']}")
    print(f"  Standard : {standard}")
    for k, v in params.items():
        print(f"  {k.replace('_', ' ').title():<11}: {v}")
    print(f"{'=' * 56}")

    confirmed = _confirm("Proceed with deployment? (gas fees apply)", default=True)
    if not confirmed:
        print(f"{YELLOW}Deployment cancelled.{RESET}")
        sys.exit(0)

    print(f"\n{CYAN}>>> Deploying contract...{RESET}\n")

    try:
        if standard == "ERC-20":
            result = deploy_erc20(
                rpc_url=network["rpc"],
                private_key=private_key,
                name=params["name"],
                symbol=params["symbol"],
                decimals=params["decimals"],
                initial_supply=params["initial_supply"],
            )
        else:
            result = deploy_erc721(
                rpc_url=network["rpc"],
                private_key=private_key,
                name=params["name"],
                symbol=params["symbol"],
            )
    except Exception as exc:
        print(f"{RED}[FAIL] Deployment failed: {exc}{RESET}")
        sys.exit(1)

    print(f"{GREEN}{'=' * 56}{RESET}")
    print(f"{GREEN}{BOLD}  [OK] Token deployed successfully!{RESET}")
    print(f"{GREEN}{'=' * 56}{RESET}")
    print(f"  Contract Address  : {GREEN}{result['contract_address']}{RESET}")
    print(f"  Transaction Hash  : {result['transaction_hash']}")
    print(f"  Gas Used          : {result['gas_used']:,}")
    print(f"  Block Number      : {result['block_number']:,}")

    if network.get("explorer"):
        url = f"{network['explorer']}/address/{result['contract_address']}"
        print(f"  Explorer          : {CYAN}{url}{RESET}")

    if standard == "ERC-721":
        print()
        print(f"{YELLOW}TIP: Next step:{RESET}")
        print("   Use the mint() function to create individual NFTs.")
        print("   1) Upload metadata JSON to IPFS (or any URI-accessible storage)")
        print('   2) Call mint(recipient, "ipfs://...") on the contract above.')

    print()


# ── Main ──────────────────────────────────────────────────────────────────


def main() -> None:
    _print_banner()
    network = _choose_network()
    standard = _choose_standard()

    if standard == "ERC-20":
        params = _ask_erc20_params()
    else:
        params = _ask_erc721_params()

    private_key = _ask_private_key()

    _confirm_and_deploy(
        network=network,
        standard=standard,
        params=params,
        private_key=private_key,
    )


if __name__ == "__main__":
    main()
