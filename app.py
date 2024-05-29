import web3
import json
import yaml
import time
import random

from utils.open_abi import read_abi
from utils.interaction import interact, read_function_from_contract

from web3 import Web3, AsyncWeb3
from web3.gas_strategies.rpc import rpc_gas_price_strategy


faucet_abi = read_abi("abi/faucet_abi.json")
main_abi = read_abi("abi/main_abi.json")
chainlink_abi = read_abi("abi/chainlink_abi.json")
bridge_abi = read_abi("abi/bridge_abi.json")


with open('env.yaml', 'r') as file:
    env = yaml.safe_load(file)

faucet_address = env["faucet_address"]
main_contract_address = env["main_contract_address"]
bridge_contract = env["bridge_contract"]

account_address = env["account_address"]
private_key = env["private_key"]
url = env["arbitrum_sepolia_url"]

web3_client = Web3(Web3.HTTPProvider(url))
web3_client.eth.set_gas_price_strategy(
    rpc_gas_price_strategy
)

faucet_ammount = env["synthr_faucet_token_amount"]
lz_value = env["lz_value"]
lz_value_burn = env["lz_value_burn"]
lz_value_wd = env["lz_value_wd"]

default_gas = 4000000 + random.randint(1, 100)
default_gas_price = web3_client.eth.gas_price
default_gas_price = Web3.to_wei("1.6", "gwei")


while True:
    # Claim Faucet
    interact(
        web3_client=web3_client,
        contract_address=Web3.to_checksum_address(faucet_address),
        function_name="faucetToken",
        abi=faucet_abi, 
        account_address=account_address,
        private_key=private_key,
        function_args=(faucet_ammount,), 
        gas=default_gas, 
        gas_price=default_gas_price,
        lz_value=lz_value_burn
    )

    time.sleep(1.5)
    # Approve transactions
    interact(
        web3_client=web3_client, 
        contract_address=faucet_address, 
        function_name="approve", 
        abi=faucet_abi, 
        account_address=account_address, 
        private_key=private_key, 
        function_args=(
            main_contract_address, 
            115792089237316195423570985008687907853269984665640564039457584007913129639935,
            ), 
        gas=default_gas, 
        gas_price=default_gas_price, 
        lz_value=lz_value_burn
    )

    time.sleep(1.5)
    # # Add Collateral
    interact(
        web3_client=web3_client, 
        contract_address=main_contract_address, 
        function_name="issueSynths", 
        abi=main_abi, 
        account_address=account_address, 
        private_key=private_key, 
        function_args=(
            "0x4545544800000000000000000000000000000000000000000000000000000000",
            faucet_ammount,
            0,
            "0x4c617965725a65726f0000000000000000000000000000000000000000000000",
            0,
            False,
        ), 
        gas=default_gas,
        gas_price=default_gas_price,
        lz_value=lz_value_burn
    )

    time.sleep(1.5)
    # # Mint syUSD
    issue_amount = int(1e18 * 10_000) + random.randint(
            0, int(1e8)
        )
    interact(
        web3_client=web3_client, 
        contract_address=main_contract_address, 
        function_name="issueSynths", 
        abi=main_abi, 
        account_address=account_address, 
        private_key=private_key, 
        function_args=(
                    "0x0000000000000000000000000000000000000000000000000000000000000000",
                    0,
                    issue_amount,
                    "0x4c617965725a65726f0000000000000000000000000000000000000000000000",
                    0,
                    False,
        ),
        gas=default_gas,
        gas_price=default_gas_price,
        lz_value=lz_value_burn
    )

    time.sleep(1.5)
    # # Same chain swap
    eth_usd_chainlink_feed = "0xd30e2101a97dcbAeBCBC04F14C3f624E67A35165"
    eth_usd_price_raw = read_function_from_contract(
                            web3_client=web3_client,
                            contract_address=eth_usd_chainlink_feed,
                            function_name="latestAnswer",
                            abi=chainlink_abi,
                        ).call()
    eth_usd_price = int(eth_usd_price_raw) / 1e8 if eth_usd_price_raw != 0 else 0
    usd_eth_price = 1 / eth_usd_price

    interact(
        web3_client=web3_client, 
        contract_address=main_contract_address, 
        function_name="exchangeAtomically", 
        abi=main_abi, 
        account_address=account_address, 
        private_key=private_key, 
        function_args=(
                    "0x7355534400000000000000000000000000000000000000000000000000000000",
                    int(10 * 1e18),  # 10 sUSD
                    "0x7345544800000000000000000000000000000000000000000000000000000000",
                    int(usd_eth_price * 10 * 1e18)
                    - 68014044637676,
                    "0x4c617965725a65726f0000000000000000000000000000000000000000000000",
                    0,
                    False,
        ),
        gas=default_gas,
        gas_price=default_gas_price,
        lz_value=lz_value
    )

    time.sleep(1.5)
    # Burn syUSD
    interact(
        web3_client=web3_client, 
        contract_address=main_contract_address, 
        function_name="burnSynths", 
        abi=main_abi, 
        account_address=account_address, 
        private_key=private_key, 
        function_args=(
                    10000000000000000000,
                    "0x7355534400000000000000000000000000000000000000000000000000000000",
                    "0x4c617965725a65726f0000000000000000000000000000000000000000000000",
        ),
        gas=default_gas,
        gas_price=default_gas_price,
        lz_value=lz_value_burn
    )

    time.sleep(1.5)
    interact(
    web3_client=web3_client, 
    contract_address=main_contract_address, 
    function_name="withdrawCollateral", 
    abi=main_abi, 
    account_address=account_address, 
    private_key=private_key, 
    function_args=(
                "0x4545544800000000000000000000000000000000000000000000000000000000",
                10000000000000000,
                "0x4c617965725a65726f0000000000000000000000000000000000000000000000",
                0,
                False,
    ),
    gas=default_gas,
    gas_price=default_gas_price,
    lz_value=lz_value_wd
)