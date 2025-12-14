import os
import json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
raw_address = os.getenv("WALLET_ADDRESS")
FROM_ADDRESS = Web3.to_checksum_address(raw_address) if raw_address else None

web3 = Web3(Web3.HTTPProvider(RPC_URL))

def check_connection():
    return web3.is_connected()

def get_balance():
    if not FROM_ADDRESS: return 0.0
    bal = web3.eth.get_balance(FROM_ADDRESS)
    return float(web3.from_wei(bal, 'ether'))

def load_contract():
    if not os.path.exists("contract_config.json"):
        return None
    with open("contract_config.json", "r") as f:
        config = json.load(f)
    return web3.eth.contract(address=config["address"], abi=config["abi"])

def buy_item_on_chain(item_id, price_eth, seller_address="0x000000000000000000000000000000000000dEaD"):
    if not check_connection():
        return {"status": "error", "message": "Blockchain not connected"}

    contract = load_contract()
    if not contract:
        return {"status": "error", "message": "Contract not deployed (run deploy.py)"}

    try:
        nonce = web3.eth.get_transaction_count(FROM_ADDRESS)
        value_wei = web3.to_wei(price_eth, 'ether')
        
        tx = contract.functions.buyItem(
            Web3.to_checksum_address(seller_address), 
            str(item_id)
        ).build_transaction({
            'chainId': 97,
            'gas': 300000,
            'gasPrice': web3.eth.gas_price,
            'nonce': nonce,
            'value': value_wei
        })

        signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

        return {
            "status": "success",
            "tx_hash": web3.to_hex(tx_hash),
            "message": f"Smart Contract Purchase Executed! (Item {item_id})"
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}