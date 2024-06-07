import web3
from web3 import Web3, AsyncWeb3
from web3.gas_strategies.rpc import rpc_gas_price_strategy

def interact(web3_client, contract_address, function_name, abi, account_address, 
             private_key, function_args, gas, gas_price):
    
    contract = web3_client.eth.contract(
        address=web3_client.to_checksum_address(contract_address), abi=abi
    )
    while True:
        try:
            trx = contract.functions[function_name](*function_args).build_transaction({
            "from": account_address,
            "nonce": web3_client.eth.get_transaction_count(account_address),
            "gas": gas, # re-enable if you don't want it to automatically match network gas
            "gasPrice": gas_price,
            })

            signed_txn = web3_client.eth.account.sign_transaction(trx, private_key)
            txn_hash = web3_client.eth.send_raw_transaction(signed_txn.rawTransaction)
            check_transaction_status(web3_client, txn_hash, function_name)

            break
        except Exception as e:
            print(f"Error {e} mencoba ulang {function_name} ...")



def interact_burn(web3_client, contract_address, function_name, abi, account_address, 
             private_key, function_args, gas, gas_price):
    
    contract = web3_client.eth.contract(
        address=web3_client.to_checksum_address(contract_address), abi=abi
    )
    while True:
        try:
            trx = contract.functions[function_name](*function_args).build_transaction({
            "from": account_address,
            "nonce": web3_client.eth.get_transaction_count(account_address),
            "gas": gas, # re-enable if you don't want it to automatically match network gas
            "gasPrice": gas_price,
            "value": web3_client.to_wei(0.0, "ether"),
            })

            signed_txn = web3_client.eth.account.sign_transaction(trx, private_key)
            txn_hash = web3_client.eth.send_raw_transaction(signed_txn.rawTransaction)
            check_transaction_status(web3_client, txn_hash, function_name)

            break
        except Exception as e:
            print(f"Error {e} mencoba ulang {function_name} ...")


def interact_bridge(web3_client, contract_address, function_name, abi, account_address, 
                    private_key, function_args, gas, gas_price, lz_value):

    contract = web3_client.eth.contract(
        address=web3_client.to_checksum_address(contract_address), abi=abi
    )
    while True:
        try:
            trx = contract.functions[function_name](*function_args).build_transaction({
                "from": account_address,
                "nonce": web3_client.eth.get_transaction_count(account_address),
                "gas": gas, # re-enable if you don't want it to automatically match network gas
                "gasPrice": gas_price,
                "value": web3_client.to_wei(lz_value, "ether"),
                })

            signed_txn = web3_client.eth.account.sign_transaction(trx, private_key)
            txn_hash = web3_client.eth.send_raw_transaction(signed_txn.rawTransaction)
            check_transaction_status(web3_client, txn_hash, function_name)

            break
        except Exception as e:
            print(f"Error {e} mencoba ulang...")


def check_transaction_status(web3_client, txn_hash, function_name) -> int:
    while True:
        try:
            txn_receipt = web3_client.eth.get_transaction_receipt(txn_hash)
            if txn_receipt is not None:
                print(f"Success trx: {function_name}")
                break
        except Exception as e:
            print(f"Error checking transaction status {e}")


def read_function_from_contract(web3_client, contract_address: str, function_name: str, abi: dict, *args):
    contract = web3_client.eth.contract(
        address=web3_client.to_checksum_address(contract_address), abi=abi
    )
    return contract.functions[function_name](*args)