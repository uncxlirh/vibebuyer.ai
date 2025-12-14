import json
import os
from web3 import Web3
from dotenv import load_dotenv
from solcx import compile_standard, install_solc

load_dotenv()

install_solc('0.8.0')

with open("./contracts/VibeMarket.sol", "r") as file:
    vibe_market_file = file.read()

print("Compiling contract...")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"VibeMarket.sol": {"content": vibe_market_file}},
        "settings": {"outputSelection": {"*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}}},
    },
    solc_version="0.8.0",
)

bytecode = compiled_sol["contracts"]["VibeMarket.sol"]["VibeMarket"]["evm"]["bytecode"]["object"]
abi = compiled_sol["contracts"]["VibeMarket.sol"]["VibeMarket"]["abi"]

w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))
chain_id = 97
my_address = w3.to_checksum_address(os.getenv("WALLET_ADDRESS"))
private_key = os.getenv("PRIVATE_KEY")

print(f"Deploying from {my_address}...")

VibeMarket = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.get_transaction_count(my_address)

transaction = VibeMarket.constructor().build_transaction({
    "chainId": chain_id,
    "gasPrice": w3.eth.gas_price,
    "from": my_address,
    "nonce": nonce
})

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

print(f"Tx sent! Hash: {tx_hash.hex()}")
print("Waiting for confirmation...")

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(f"✅ Contract Deployed at: {tx_receipt.contractAddress}")

config = {"address": tx_receipt.contractAddress, "abi": abi}
with open("contract_config.json", "w") as f:
    json.dump(config, f)