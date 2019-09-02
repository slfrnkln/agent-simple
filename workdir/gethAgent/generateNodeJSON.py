import json
from web3 import Web3

#edit addresses down below to add test FET to correct accounts, ETH accounts connected with your agents

#my_provider = Web3.HTTPProvider("http://127.0.0.1:8080") #8545, 30303
#w3 = Web3(my_provider)

address1 = "0xC7f8c7e9B41d97B431fD05168aFE70a64C50aCF1" #w3.eth.accounts[0] #"0x41FD089BD912da31b704fc36fdE2d1486E1551B1"

x = {
 "config": {
  "chainId": 15,
  "homesteadBlock": 0,
  "eip155Block": 0,
  "eip158Block": 0
 },
 "nonce": "0x0000000000000042",
 "timestamp": "0x0",
 "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
 "gasLimit": "0x8000000",
 "difficulty": "0x400",
 "mixhash": "0x0000000000000000000000000000000000000000000000000000000000000000",
 "coinbase": "0x3333333333333333333333333333333333333333",
 "alloc": {
  address1: {
  "balance": "0x9999000000000000000000"},
 }
}

with open('./mychain/nodeJSON.json', 'w') as customNodeJSON:
    json.dump(x, customNodeJSON)

print(json.dumps(x))
