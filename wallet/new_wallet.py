#!/usr/bin/env python3
"""
Generate a fresh Ethereum wallet for testing purposes.

Usage:
    python new_wallet.py
"""

from web3 import Web3

account = Web3().eth.account.create()

print()
print("  New wallet generated:\n")
print(f"  Address:      {account.address}")
print(f"  Private Key:  {account.key.hex()}")
print()
print("  Next steps:")
print("  1. Copy the Address and paste it in a Sepolia faucet")
print("     https://sepolia-faucet.pk910.de")
print("     https://www.alchemy.com/faucets/ethereum-sepolia")
print("  2. Once you receive test ETH, use the Private Key in TokenForge")
print()
