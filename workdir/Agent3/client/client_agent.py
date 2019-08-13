
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


class ClientAgent(OEFAgent):
    """
    The class that defines the behaviour of the echo client agent.
    """
    def __init__(self, public_key: str, price: int, account: Entity, oef_addr: str, oef_port: int = 10000):
        super().__init__(public_key, oef_addr, oef_port, loop=asyncio.new_event_loop())
        self.cost = 0
        self.pending_cfp = 0
        self.received_proposals = []
        self.received_declines = 0

        self.account = account
        self.highest_price = price
        self.currentPrice = 0
        self.proposalsTot = 0
        self.prevPrice = 0

        self.api = LedgerApi('127.0.0.1', 8100)

    def reduceOffer(self, value: int):

        print('Halved Offer')
        price = (value/2)
        print('----->PRICE:', price)
        if price <= self.highest_price:
            self.currentPrice = price
        else:
            self.reduceOffer(price)

    def on_message(self, msg_id: int, dialogue_id: int, origin: str, content: bytes):
        print("Received message: origin={}, dialogue_id={}, content={}".format(origin, dialogue_id, content))
        data = json.loads(content.decode())
        print ("message...")
        print(data)
        print('Final Balance:', self.api.tokens.balance(self.account))
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

        self.proposalsTot = self.proposalsTot + 1

        # once everyone has responded, let's accept them.
        print("I am here")
        if len( self.received_proposals) >= 1 :
            proposed = str(self.received_proposals[self.proposalsTot-1]['proposal'])
            price = int(self.received_proposals[self.proposalsTot-1]['proposal']['price'])
            print('----->PRICE:', price)
            if price <= self.highest_price:
                print('Accept the offer!')
                #check if we can afford the data.
                if self.api.tokens.balance(self.account) > price :
                    #if we can, transfer tokens from the client account to the proposal address.
                    self.api.sync(self.api.tokens.transfer(self.account, Address(self.received_proposals[self.proposalsTot-1]['agent']) , price, 20))
                    self.send_accept(msg_id,dialogue_id,self.received_proposals[self.proposalsTot-1]['agent'],msg_id + 1)
                    print ("Accept")
                else :
                    print("Not enough tokens!")
                    #cannot afford! Decline the proposal.
                    self.send_decline(msg_id,dialogue_id,self.received_proposals[self.proposalsTot-1]['agent'],msg_id + 1)

                    self.stop()
            elif price == self.prevPrice:
                print('They are sticking with offer, better offer higher...')
                proposal = Description({"price" : self.highest_price})
                print("[{0}]: Sending propose at price: {1}".format(self.public_key, self.highest_price))
                self.send_propose(msg_id + 1, dialogue_id, origin, target + 1, [proposal])
            else:
                print('Too Expensive, want lower!')
                self.prevPrice = price
                self.reduceOffer(price)
                price = self.currentPrice
                proposal = Description({"price" : price})
                print("[{0}]: Sending propose at price: {1}".format(self.public_key, price))
                self.send_propose(msg_id + 1, dialogue_id, origin, target + 1, [proposal])
        else :
            print("They don't have data")
            self.stop()

    def on_decline(self, msg_id: int, dialogue_id: int, origin: str, target: int) :
        print("Received a decline!")
        self.received_declines += 1
        return

if __name__ == '__main__':

    #define the ledger parameters
    api = LedgerApi('127.0.0.1', 8100)

    #check if entity has already been created
    if(os.path.exists('./workdir/Agent3/client/client_private.key')):

        #locate the agent account entity for interacting with the ledger.
        with open ('./workdir/Agent3/client/client_private.key', 'r') as private_key_file:
                client_agentID = Entity.load(private_key_file)

    else:
        #create new entity for the agent
        client_agentID = Entity()
        #store private key of newly formed entity
        with open('./workdir/Agent3/client/client_private.key', 'w') as private_key_file:
            client_agentID.dump(private_key_file)
        #give the account starting tokens
        api.sync(api.tokens.wealth(client_agentID, 1000))

    startBalance = api.tokens.balance(client_agentID)

    highest_price = 1000

    # define an OEF Agent
    client_agent = ClientAgent(str(Address(client_agentID)), highest_price, client_agentID, oef_addr="127.0.0.1", oef_port=10000)

    print('Balance Before:', startBalance)

    # connect it to the OEF Node
    client_agent.connect()

    # query OEF for DataService providers
    echo_query1 = Query([Constraint("timezone", Eq(3)), Constraint("twentyfour", Eq(False))],TIME_AGENT())


    client_agent.search_services(0, echo_query1)
    client_agent.run()
