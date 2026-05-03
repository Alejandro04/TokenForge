# Wallet Utilities

Scripts to generate and manage Ethereum wallets for testing.

## Files

| File | Purpose |
|------|---------|
| `new_wallet.py` | Generate a fresh Ethereum keypair for testnet use |

## Quick Start

```bash
python wallet/new_wallet.py
```

Run this **every time** you need a new test wallet. The script creates a public/private keypair using `web3.py`'s built-in entropy source — no external node or network connection required.

## Output

```
New wallet generated:

  Address:      0x8a53f6Ab0aa84030DC5942F017FBd9708eD443BE
  Private Key:  fb66c315c089fc87e0d7b3970091918712aba5dc6c8337ae31c1565d6d5e7b1c
```

## Next Steps (Testnet Flow)

1. Copy the **Address** and request test ETH from a faucet:
   - [Sepolia Faucet (PoW)](https://sepolia-faucet.pk910.de)
   - [Alchemy Sepolia Faucet](https://www.alchemy.com/faucets/ethereum-sepolia)
   - [Google Cloud Faucet](https://cloud.google.com/application/web3/faucet/ethereum/sepolia)

2. Wait for the transaction to confirm (usually under 1 minute).

3. Use the **Private Key** when TokenForge asks for it.

4. After deployment, **discard the wallet** — it was only funded with test ETH and holds no real value.

## Security

- These wallets are for **testnets only**.
- Never reuse a test wallet for mainnet — key management hygiene applies regardless of value.
- The private key is displayed in plain text on screen. Close your terminal or clear the scrollback after noting it down.

## Why a Dedicated Tool?

Browser extensions (MetaMask, Rabby) generate wallets too, but having a CLI utility saves the copy-paste cycle and keeps the workflow fully inside the terminal.
