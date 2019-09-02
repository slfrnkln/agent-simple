import oef
from oef.agents import OEFAgent

import os, sys
import json
import time

from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import SmartContract
from fetchai.ledger.crypto import Entity, Address, Identity

from oef.proxy import  OEFProxy, PROPOSE_TYPES
from oef.query import Eq, Range, Constraint, Query, AttributeSchema, Distance
from oef.schema import DataModel, Description , Location
from oef.messages import CFP_TYPES

import agent_dataModel
from agent_dataModel import TIME_AGENT

import random
import json
import datetime
import copy
import getpass
import asyncio

import uuid
import time

from web3 import Web3
from transferETH import transferETH
#from solc import compile_standard

class Demo_Agent(OEFAgent):

    def __init__(self, public_key: str, oef_addr: str, oef_port: int = 10000):
        super().__init__(public_key, oef_addr, oef_port, loop=asyncio.new_event_loop())

        self.scheme = {}
        self.scheme['timezone'] = None
        self.scheme['id'] = None

    def on_cfp(self, msg_id: int, dialogue_id: int, origin: str, target: int, query: CFP_TYPES):
        """Send a simple Propose to the sender of the CFP."""
        print("[{0}]: Received CFP from {1}".format(self.public_key, origin))

        #format the price for number extraction on other agent
        proposal = Description({"price" : price, "account" : acc_ETH})
        print("[{0}]: Sending propose at price: {1} FET".format(self.public_key, price))
        self.send_propose(msg_id + 1, dialogue_id, origin, target + 1, [proposal])
        startBalance = api.tokens.balance(server_agentID)

    def on_accept(self, msg_id: int, dialogue_id: int, origin: str, target: int):
        """Once we received an Accept, check the correct funds have been recieved. If so send the requested data."""
        print("[{0}]: Received accept from {1}.".format(self.public_key, origin))
        time.sleep(10)

        if startBalance + price == api.tokens.balance(server_agentID):
            command = {}
            command["time"] = int(time.time())
            msg = json.dumps(command)
            self.send_message(0,dialogue_id, origin, msg.encode())

            print('Final Balance:', api.tokens.balance(server_agentID))
        elif bal_ETH + int(w3.toWei(priceETH, 'ether')) == transferETH.getFunds(acc_ETH):
            command = {}
            command["time"] = int(time.time())
            msg = json.dumps(command)
            self.send_message(0,dialogue_id, origin, msg.encode())

            print('Final Balance:', transferETH.getFunds(acc_ETH))
            #print('bal_ETH+price', (bal_ETH + int(w3.toWei(priceETH, 'ether'))))
        else:
            print('No Funds Sent!')
            print('Ending Dialogue')
            return


    def on_decline(self, msg_id: int, dialogue_id: int, origin: str, target: int):
        print("declined")


    def on_message(self, msg_id: int, dialogue_id: int, origin: str, content: bytes):
        data = json.loads(content.decode())
        print ("message received: "  + json.dumps(data))


if __name__ == '__main__':

    #define the ledger parameters
    api = LedgerApi('127.0.0.1', 8100)

    my_provider = Web3.HTTPProvider("http://127.0.0.1:8080") #8545, 30303
    w3 = Web3(my_provider)

    #-----------------------------------------------------------

    accountAddress = ''

    #check if account has already been generated
    if(os.path.exists('./agent/account.json')):

        #load adress for ethereum account
        with open ('./agent/account.json', 'r') as account_Info:
                accountInfo = json.load(account_Info)
        accountAddress = accountInfo['address']

    print(accountAddress)
    print(w3.eth.accounts)

    #Set the account address
    if accountAddress in w3.eth.accounts:
        w3.eth.defaultAccount = accountAddress #w3.eth.accounts[0]
    #Generate a new account
    else:
        genAccount = True
        while genAccount:
            pword = getpass.getpass(prompt = 'Please enter password for new account:')
            if pword == getpass.getpass(prompt ='Please re-enter password for new account:'):
                genAccount = False
                break
            print('Passwords did not match!')
        new_account = w3.geth.personal.newAccount(pword)
        print(new_account)
        pword = ''
        w3.eth.defaultAccount = new_account
        print('Account generated!')
        #Save account information
        x = {
            "address": new_account
        }
        with open('./agent/account.json', 'w') as accountInfo:
            json.dump(x, accountInfo)

    acc_ETH = w3.eth.defaultAccount
    bal_ETH = w3.eth.getBalance(acc_ETH)

    #transfer funds from main account
    #> dont need to transfer funds to demo_agent.

    #print(accounts)
    print("ETH Account: {0} Balance: {1}".format(acc_ETH, bal_ETH))

    #checl if entity has already been generated
    if(os.path.exists('./agent/server_private.key')):

        #locate the agent account entity for interacting with the ledger.
        with open ('./agent/server_private.key', 'r') as private_key_file:
                server_agentID = Entity.load(private_key_file)

    else:
        #create the enity for the agent
        server_agentID = Entity()
        #store the private key of the newly created entity
        with open('./agent/server_private.key', 'w') as private_key_file:
            server_agentID.dump(private_key_file)

    startBalance = api.tokens.balance(server_agentID)

    #set trading values
    price = 200
    priceETH = transferETH.convertFET(price)
    fet_tx_fee = 40

    print('Price:', price)
    print('ETH price:', transferETH.convertFET(price))
    print('Balance Before:', startBalance)

    # create agent and connect it to OEF
    server_agent = Demo_Agent(str(Address(server_agentID)), oef_addr="127.0.0.1", oef_port=10000)
    server_agent.scheme['timezone'] = 3
    server_agent.scheme['id'] = str(uuid.uuid4())
    server_agent.scheme['twentyfour'] = False
    server_agent.connect()
    # register a service on the OEF
    server_agent.description = Description(server_agent.scheme, TIME_AGENT())
    server_agent.register_service(0,server_agent.description)
    server_agent.run()
