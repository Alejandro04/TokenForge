<div align="center">

```
╔══════════════════════════════════════════════════════════╗
║   ████████╗ ██████╗ ██╗  ██╗███████╗███╗   ██╗          ║
║   ╚══██╔══╝██╔═══██╗██║ ██╔╝██╔════╝████╗  ██║          ║
║      ██║   ██║   ██║█████╔╝ █████╗  ██╔██╗ ██║          ║
║      ██║   ██║   ██║██╔═██╗ ██╔══╝  ██║╚██╗██║          ║
║      ██║   ╚██████╔╝██║  ██╗███████╗██║ ╚████║          ║
║      ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝          ║
╚══════════════════════════════════════════════════════════╝
</div>

---

**Tokenize real‑world assets on any EVM blockchain — from the command line.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://python.org)

</div>

---

## 📖 What Is TokenForge?

TokenForge is an **open‑source CLI tool** that lets anyone deploy
[ERC‑20](https://eips.ethereum.org/EIPS/eip-20) (fungible) and
[ERC‑721](https://eips.ethereum.org/EIPS/eip-721) (non‑fungible) token
contracts on any EVM‑compatible blockchain.

It was built for **small businesses, lawyers, developers, and creators**
who want to tokenize assets — real estate, invoices, carbon credits, art,
commodities, equity — without depending on expensive SaaS platforms.

No web dashboard. No hidden fees. Just a terminal wizard that asks a few
questions and then deploys the contract directly to your chosen network.

> ⚡ **MVP Status** — TokenForge currently supports ERC‑20 and ERC‑721.
> [ERC‑3643](https://eips.ethereum.org/EIPS/eip-3643) (permissioned
> security tokens with on‑chain compliance) is on the roadmap.

---

## 🧠 Why TokenForge?

| 🚫 Without TokenForge | ✅ With TokenForge |
|---|---|
| Pay $500–$5,000+ to tokenization platforms per deployment | Free. MIT‑licensed. |
| Locked into one vendor’s smart contracts | You own the contract. You hold the private key. |
| Sift through 200‑line web forms | 5 questions in a terminal wizard. |
| Can’t audit what’s deployed | Solidity sources are right here. Read them. |
| Deployments limited to one chain | Multi‑chain from day one (Ethereum, Polygon, Arbitrum, Base, …). |

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** The first run will automatically download the Solidity compiler
> (`solc` v0.8.20) via `py-solc-x`. This is a one‑time ~20 MB download.

### 2. Run the wizard

```bash
python tokenforge.py
```

### 3. Answer the prompts

```
Select network → Sepolia Testnet (for testing)
Token standard → ERC-20
Name           → MyCompany Gold
Symbol         → MCG
Decimals       → 18
Initial supply → 1_000_000
Private key    → 0x…
Confirm?       → Yes
```

### 4. Done

```
✅  Token deployed successfully!
   Contract Address  : 0xAbCd…1234
   Transaction Hash  : 0x…
   Explorer          : https://sepolia.etherscan.io/address/0xAbCd…1234
```

Your token is now live and you hold the full supply.

---

## 🗂️ Architecture

```
tokenforge/
├── tokenforge.py            # CLI wizard (entry point)
├── requirements.txt
├── .gitignore
├── README.md
└── forge/
    ├── __init__.py          # Package metadata
    ├── contracts.py          # Solidity source code (ERC‑20 & ERC‑721)
    ├── compiler.py           # solc compilation wrapper
    └── deployer.py           # Web3 deployment logic
```

```
                         ┌──────────────────┐
                         │   tokenforge.py  │
                         │  (CLI Wizard)    │
                         └────────┬─────────┘
                                  │ asks for
                ┌─────────────────┼─────────────────┐
                ▼                 ▼                  ▼
         ┌─────────────┐  ┌─────────────┐   ┌──────────────┐
         │ compiler.py │  │ deployer.py │   │ contracts.py │
         │ (solc)      │  │ (web3.py)   │   │ (Solidity)   │
         └──────┬──────┘  └──────┬──────┘   └──────────────┘
                │                │
                ▼                ▼
         ┌──────────────────────────────────┐
         │          EVM Blockchain          │
         │  (ETH, Polygon, Arbitrum, …)     │
         └──────────────────────────────────┘
```

---

## 🔧 Supported Standards

| Standard | Type | MVP | Features |
|----------|------|:---:|----------|
| **ERC-20** | Fungible | ✅ | Transfer, approve, transferFrom. Full supply minted to deployer. |
| **ERC-721** | Non‑Fungible | ✅ | Mint‑on‑demand, per‑token metadata URI, approvals. |
| **ERC-3643** | Security Token | 🔜 | On‑chain identity whitelisting, transfer restrictions, forced transfers. |
| **ERC-1155** | Multi‑Token | 🔜 | Single contract for fungible + non‑fungible tokens. |
| **ERC-4626** | Vaults | 🔜 | Yield‑bearing tokenized vaults (treasury bills, staking). |

### Included Networks

| Network | Type |
|---------|------|
| Ethereum Mainnet | Mainnet |
| Polygon Mainnet | Mainnet |
| Arbitrum One | Mainnet |
| Base | Mainnet |
| Sepolia Testnet | Testnet |
| Amoy Testnet (Polygon) | Testnet |
| *Custom RPC* | Any EVM chain |

---

## ⚖️ Compliance & Legal Considerations

> **TokenForge is a technical tool — it is NOT legal advice.**

When you tokenize an asset, you may be creating a **security** under the
laws of your jurisdiction. You are solely responsible for understanding
and complying with applicable regulations.

### What you must evaluate before deploying

| Concern | What to Ask Your Lawyer |
|---------|------------------------|
| **Security classification** | Does my token pass the [Howey Test](https://www.investor.gov/introduction-investing/investing-basics/glossary/howey-test) (US)? Is it a financial instrument under [MiCA](https://www.esma.europa.eu/esmas-activities/digital-finance-and-innovation/markets-crypto-assets-regulation-mica) (EU)? |
| **KYC / AML** | Am I required to verify the identity of every token holder? |
| **Transfer restrictions** | Can I legally allow secondary trading? Do I need a lock‑up period? |
| **Accredited investors** | Must my buyers qualify under [Regulation D](https://www.sec.gov/resources-small-businesses/small-business-compliance-guides/regulation-d-offerings) (US)? |
| **Disclosures** | What documents must I provide to buyers (PPM, whitepaper, risk disclosures)? |
| **Taxation** | Are token transfers taxable events? What about yield / dividends? |
| **Data privacy** | If I store metadata on IPFS, does it contain PII? Is that GDPR‑compliant? |

### What TokenForge does NOT do (yet)

- ❌ Enforce on‑chain KYC/AML checks
- ❌ Restrict transfers to whitelisted addresses
- ❌ Force a lock‑up or vesting schedule
- ❌ Generate legal documents (PPM, terms & conditions)
- ❌ Integrate with identity oracles (Chainlink, Polygon ID)

> These features are the core of **ERC‑3643** — the standard for
> permissioned security tokens. Roadmap item.

### Recommended path for real‑world asset tokenization

1. **Consult a securities lawyer** in your jurisdiction.
2. **Use a testnet** (Sepolia, Amoy) for all experiments.
3. **Start with simple assets** where tokenization is well‑tested (art, collectibles, loyalty points).
4. **Upgrade to ERC‑3643** (coming to TokenForge) when you need on‑chain compliance.

---

## 📋 Roadmap

- [x] ERC‑20 deployment wizard
- [x] ERC‑721 deployment wizard
- [x] Multi‑chain support (6 networks + custom RPC)
- [ ] ERC‑3643 (T‑REX) security token standard
- [ ] Batch minting UI (mint many NFTs at once)
- [ ] IPFS metadata upload helper
- [ ] Contract verification script (Etherscan / Sourcify)
- [ ] ERC‑1155 multi‑token standard
- [ ] ERC‑4626 vault standard
- [ ] Multi‑sig deployment support (Safe / Gnosis)
- [ ] Plugin system for custom token logic
- [ ] Unit test suite
- [ ] CI/CD pipeline

---

## 🤝 Contributing

Pull requests are welcome. Areas where help is especially valuable:

- **ERC‑3643 implementation** (the permissioned security token standard)
- **Unit tests** for the compiler and deployer modules
- **New EVM networks** (add them to `tokenforge.py` → `NETWORKS`)
- **Multi‑language support** for the CLI wizard

Please open an issue before submitting large changes to discuss the
approach.

---

## 📄 License

MIT © 2026 — TokenForge contributors.

The Solidity contracts included in this repository are also MIT‑licensed
and derived from [OpenZeppelin](https://openzeppelin.com/) patterns.

---

<div align="center">

*Built with Python 🐍, Solidity ⚙️, and belief that tokenization should be free.*

</div>
