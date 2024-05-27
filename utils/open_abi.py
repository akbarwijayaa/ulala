import json

def read_abi(abi_dir):
    with open(abi_dir, "r") as f:
        abi = json.load(f)
    return abi