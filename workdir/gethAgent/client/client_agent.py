
from typing import List

import oef
from oef.agents import OEFAgent
from oef.proxy import  OEFProxy, PROPOSE_TYPES
from oef.query import Eq, Range, Constraint, Query, AttributeSchema, Distance
from oef.schema import DataModel, Description , Location
from oef.messages import CFP_TYPES

from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import SmartContract
from fetchai.ledger.crypto import Entity, Address, Identity

import agent_dataModel
from agent_dataModel import TIME_AGENT

import json
import datetime


import os

import sys
import time
import uuid
import asyncio
import getpass

from web3 import Web3
from transferETH import transferETH


class ClientAgent(OEFAgent):
    """
    The class that defines the behaviour of the echo client agent.
    """
    def __init__(self, public_key: str, oef_addr: str, oef_port: int = 10000):
        super().__init__(public_key, oef_addr, oef_port, loop=asyncio.new_event_loop())
        self.cost = 0
        self.pending_cfp = 0
        self.received_proposals = []
        self.received_declines = 0


    def on_message(self, msg_id: int, dialogue_id: int, origin: str, content: bytes):
        print("Received message: origin={}, dialogue_id={}".format(origin, dialogue_id))
        data = json.loads(content.decode())
        print ("message...")
        print(data)
        print('Final Balance:', api.tokens.balance(client_agentID))
        print('Final ETH:', transferETH.getFunds(acc_ETH))
        time.sleep(10)
        self.stop()

    def on_search_result(self, search_id: int, agents: List[str]):
        """For every agent returned in the service search, send a CFP to obtain resources from them."""
        if len(agents) == 0:
            print("[{}]: No agent found. Stopping...".format(self.public_key))
            self.stop()
            return

        print("[{0}]: Agent found: {1}".format(self.public_key, agents))

        for agent in agents:

            print("[{0}]: Sending to agent {1}".format(self.public_key, agent))
            self.pending_cfp += 1
            self.send_cfp(1, 0, agent, 0, None)

    def on_propose(self, msg_id: int, dialogue_id: int, origin: str, target: int, proposals: PROPOSE_TYPES):
        """When we receive a Propose message, check if we can afford the data. If so we accept, else we decline the proposal."""
        print("[{0}]: Received propose from agent {1}".format(self.public_key, origin))

        for i,p in enumerate(proposals):
            self.received_proposals.append({"agent" : origin,
                                            "proposal":p.values})

        received_cfp = len(self.received_proposals) + self.received_declines

        #sort the multiple proposals by price
        self.received_proposals.sort(key = lambda i: (i['proposal']['price']))

        # once everyone has responded, let's accept them.
        if received_cfp == self.pending_cfp :
            print("I am here")
            if len( self.received_proposals) >= 1 :
                proposed = str(self.received_proposals[0]['proposal'])
                #price = [int(s) for s in proposed.split() if s.isdigit()]
                priceFET = self.received_proposals[0]['proposal']['price']
                priceETH = int( w3.toWei(transferETH.convertFET(self.received_proposals[0]['proposal']['price']), 'ether'))
                #check if we can afford the data.
                print('----------------------------------------------------------------')
                print('Current Price FET:{0} Current Price ETH:{1}'.format(priceFET, priceETH))
                print('Current Balance FET:{0} Current Balance ETH:{1}'.format(api.tokens.balance(client_agentID), w3.eth.getBalance(w3.eth.defaultAccount)))
                p = input('Pay with FET or ETH?')
                if p.upper() == "FET":
                    if api.tokens.balance(client_agentID) > priceFET :
                        #if we can, transfer tokens from the client account to the proposal address.
                        api.sync(api.tokens.transfer(client_agentID, Address(self.received_proposals[0]['agent']) , priceFET, 20))
                        #transfer.transaction('FET',self.public_key, Address(self.received_proposals[0]['agent']), self.received_proposals[0]['proposal']['price'])
                        self.send_accept(msg_id,dialogue_id,self.received_proposals[0]['agent'],msg_id + 1)
                        print ("Accept")
                        return
                if p.upper() == "ETH":
                    if bal_ETH > priceETH :
                        #if we can, transfer tokens from the client account to the proposal address.
                        transaction = { 'from' : w3.eth.defaultAccount, 'to' : self.received_proposals[0]['proposal']['account'], 'value' : priceETH }
                        print('----------------------------------------------------------------')
                        print(transaction)
                        print('----------------------------------------------------------------')
                        #w3.geth.personal.unlockAccount(w3.eth.defaultAccount, 'Password1!')
                        pword = getpass.getpass(prompt = 'Please type your password:')
                        w3.geth.personal.sendTransaction(transaction, pword)
                        #transfer.transaction('ETH',acc_ETH, w3.eth.accounts[0], int(transfer.convertFET('ETH', self.received_proposals[0]['proposal']['price'])* (1000000000000000000)))
                        self.send_accept(msg_id,dialogue_id,self.received_proposals[0]['agent'],msg_id + 1)
                        print ("Accept")
                        return
                print("Not enough tokens!")
                #cannot afford! Decline the proposal.
                self.send_decline(msg_id,dialogue_id,self.received_proposals[0]['agent'],msg_id + 1)
                self.stop()
            else :
                print("They don't have data")
                self.stop()

    def on_decline(self, msg_id: int, dialogue_id: int, origin: str, target: int) :
        print("Received a decline!")
        self.received_declines += 1

if __name__ == '__main__':

    #define the ledger parameters
    api = LedgerApi('127.0.0.1', 8100)

    my_provider = Web3.HTTPProvider("http://127.0.0.1:8080")
    w3 = Web3(my_provider)

    #----------------------------------------------------------------

    accountAddress = ''

    #check if account has already been generated
    if(os.path.exists('./client/account.json')):

        #load adress for ethereum account
        with open ('./client/account.json', 'r') as account_Info:
                accountInfo = json.load(account_Info)
        accountAddress = accountInfo['address']

    print(accountAddress)
    print(w3.eth.accounts)

    #accountAddress = '0x41FD089BD912da31b704fc36fdE2d1486E1551B1'

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
        with open('./client/account.json', 'w') as accountInfo:
            json.dump(x, accountInfo)

        #transfer funds from main account
        transferETH.createFunds(new_account, 200000000000000000000)#transfer 200 ether
        time.sleep(10)

    acc_ETH = w3.eth.defaultAccount
    bal_ETH = w3.eth.getBalance(acc_ETH)

    if bal_ETH == 0:
        transferETH.createFunds(acc_ETH, 200000000000000000000)#transfer 200 ether
        time.sleep(10)

    #check if entity has already been created
    if(os.path.exists('./client/client_private.key')):

        #locate the agent account entity for interacting with the ledger.
        with open ('./client/client_private.key', 'r') as private_key_file:
                client_agentID = Entity.load(private_key_file)

    else:
        #create new entity for the agent
        client_agentID = Entity()
        #store private key of newly formed entity
        with open('./client/client_private.key', 'w') as private_key_file:
            client_agentID.dump(private_key_file)
        #give the account starting tokens
        api.sync(api.tokens.wealth(client_agentID, 1000))

    startBalance = api.tokens.balance(client_agentID)

    # define an OEF Agent
    client_agent = ClientAgent(str(Address(client_agentID)), oef_addr="127.0.0.1", oef_port=10000)

    print('Balance Before:', startBalance)
    print('FET balance = ETH:', transferETH.convertFET(startBalance))
    print("ETH Account:{0} Balance:{1}".format(acc_ETH, bal_ETH))

    # connect it to the OEF Node
    client_agent.connect()

    # query OEF for DataService providers
    echo_query1 = Query([Constraint("timezone", Eq(3)), Constraint("twentyfour", Eq(False))],TIME_AGENT())


    client_agent.search_services(0, echo_query1)
    client_agent.run()
