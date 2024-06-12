import web3
import json
import yaml
import time
import random
import multiprocessing

from direct import direct
from utils.open_abi import read_abi
# from utils.interaction import interact, interact_bridge, interact_burn, read_function_from_contract

from web3 import Web3, AsyncWeb3
from web3.gas_strategies.rpc import rpc_gas_price_strategy


def process():
    with open('env/wallet.yaml', 'r') as file:
        env = yaml.safe_load(file)
    direct(env)

def process2():
    with open('env/wallet2.yaml', 'r') as file:
        env2 = yaml.safe_load(file)
    direct(env2)


if __name__ == '__main__':
    trx = multiprocessing.Process(target=process)
    trx2 = multiprocessing.Process(target=process2)

    trx.start()
    trx2.start()