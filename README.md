## Clone Repository
```bash
$ git clone https://github.com/akbarwijayaa/synthr-bot-point.git
$ cd synthr-bot-point
```

## Setup env.yaml
Add env.yaml with your address, private key, dan url sepolia.
```bash
account_address: # isi dgn address kalian
private_key: # isi dgn private key kalian

arbitrum_sepolia_url: # isi dgn url arb sepolia kalian, generate pake alchemy
arbitrum_sepolia_chain_id: 421611

synthr_faucet_token_amount: 2000000000000000000 # 2eETH
lz_value: 0.0008
lz_value_burn: 0.0
lz_value_wd: 0.002

faucet_address: "0xfb2c2196831DeEb8311d2CB4B646B94Ed5eCF684"
main_contract_address: "0xe0875CBD144Fe66C015a95E5B2d2C15c3b612179"
bridge_contract: "0x2F1673beD3E85219E2B01BC988ABCc482261c38c"
```

## Conda Installation
- Go to : https://docs.anaconda.com/free/miniconda/index.html and install conda
- Open Anaconda Promt
    - Install new env: ```$ conda install --name synthr python=3.10.14```
    - Activate env: ```$ conda activate synthr```
    - Install requirement: ```$ pip install -r requirements.txt```

## Run Program
Still on Anaconda Prompt type: ```$ python app.py ```
Output running script:
```
Success trx: faucetToken
Success trx: approve
Success trx: issueSynths
``` 

## Edit the Delay (Optional)
You can edit the delay between commands in `app.py` by modifying lines 42-43:
```python
rdm_delay = 30  # Input random delay in seconds
rdm_delta = 5   # Input the maximum deviation from the delay
````

## Loop in Linux
If you want to run the script on your Linux server and automatically re-run it after an error or failure, follow these steps:
````bash
$ chmod +x loop.sh
$ ./loop.sh
````
