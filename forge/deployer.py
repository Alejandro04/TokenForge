"""
Contract deployment logic.

Handles connecting to an EVM‑compatible RPC endpoint, estimating gas,
and broadcasting the deployment transaction.
"""

from __future__ import annotations

from typing import Any

from web3 import Web3
from web3.exceptions import ContractLogicError
from web3.types import TxReceipt

from forge.compiler import compile_erc20, compile_erc721

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _connect(rpc_url: str) -> Web3:
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.is_connected():
        raise ConnectionError(f"Cannot connect to RPC endpoint: {rpc_url}")
    return w3


def _build_and_send(
    w3: Web3,
    private_key: str,
    constructor_args: tuple[Any, ...],
    abi: list,
    bytecode: str,
) -> TxReceipt:
    account = w3.eth.account.from_key(private_key)
    chain_id = w3.eth.chain_id

    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx = contract.constructor(*constructor_args).build_transaction(
        {
            "from": account.address,
            "nonce": w3.eth.get_transaction_count(account.address),
            "chainId": chain_id,
        }
    )

    # Estimate gas — fall back to a generous default if estimation fails
    try:
        tx["gas"] = int(w3.eth.estimate_gas(tx) * 1.2)
    except ContractLogicError:
        tx["gas"] = 3_000_000

    signed = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)

    return w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def deploy_erc20(
    *,
    rpc_url: str,
    private_key: str,
    name: str,
    symbol: str,
    decimals: int,
    initial_supply: int,
) -> dict[str, Any]:
    """Deploy an ERC-20 token contract.

    Returns a dict with ``contract_address``, ``transaction_hash``,
    ``gas_used``, and ``block_number``.
    """
    abi, bytecode = compile_erc20()
    w3 = _connect(rpc_url)

    receipt = _build_and_send(
        w3=w3,
        private_key=private_key,
        constructor_args=(name, symbol, decimals, initial_supply),
        abi=abi,
        bytecode=bytecode,
    )

    return {
        "standard": "ERC-20",
        "contract_address": receipt.contractAddress,  # type: ignore[attr-defined]
        "transaction_hash": receipt.transactionHash.hex(),
        "gas_used": receipt.gasUsed,
        "block_number": receipt.blockNumber,
    }


def deploy_erc721(
    *,
    rpc_url: str,
    private_key: str,
    name: str,
    symbol: str,
) -> dict[str, Any]:
    """Deploy an ERC-721 token contract.

    Returns a dict with ``contract_address``, ``transaction_hash``,
    ``gas_used``, and ``block_number``.
    """
    abi, bytecode = compile_erc721()
    w3 = _connect(rpc_url)

    receipt = _build_and_send(
        w3=w3,
        private_key=private_key,
        constructor_args=(name, symbol),
        abi=abi,
        bytecode=bytecode,
    )

    return {
        "standard": "ERC-721",
        "contract_address": receipt.contractAddress,  # type: ignore[attr-defined]
        "transaction_hash": receipt.transactionHash.hex(),
        "gas_used": receipt.gasUsed,
        "block_number": receipt.blockNumber,
    }
