
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
    def __init__(self, public_key: str, price: int, interval: int, account: Entity, oef_addr: str, oef_port: int = 10000):
        super().__init__(public_key, oef_addr, oef_port, loop=asyncio.new_event_loop())
        self.cost = 0
        self.pending_cfp = 0
        self.received_proposals = []
        self.received_declines = 0

        self.interval = interval
        self.maxPrice = price
        self.Auction = False
        self.prevPrice = 0

        self.api = LedgerApi('127.0.0.1', 8100)
        self.account = account


    def on_message(self, msg_id: int, dialogue_id: int, origin: str, content: bytes):
        data = json.loads(content.decode())
        print ("message received from {}: ".format(origin)  + json.dumps(data))

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
        for i,p in enumerate(proposals):
            self.received_proposals.append({"agent" : origin,
                                            "proposal":p.values})
            newPrice = self.received_proposals[0]['proposal']['price']
            newOffer = newPrice + self.interval
            self.prevPrice = newOffer
            if self.Auction == False:
                if self.received_proposals[0]['proposal']['auction']:
                    print('[{0}] Accepting Auction with maxPrice: {1}, at interval: {2}'.format(self.public_key, self.maxPrice, self.interval))
                    self.send_accept(msg_id, dialogue_id, self.received_proposals[0]['agent'], msg_id+1)
                    self.received_proposals.clear()
                    self.Auction = True
            else:
                if self.received_proposals[0]['proposal']['auction'] == False:
                    if newPrice <= self.maxPrice:
                        print('Accepting Offer of Price: {}'.format(newPrice))
                        self.send_accept(msg_id, dialogue_id, self.received_proposals[0]['agent'], msg_id+1)
                        self.api.sync(self.api.tokens.transfer(self.account, Address(origin) , self.prevPrice - self.interval, 20))
                        print('Final Balance:', self.api.tokens.balance(self.account))
                    else:
                        print('Cannot Afford')
                        self.send_decline(msg_id,dialogue_id,self.received_proposals['agent'],msg_id + 1)

                if newOffer <= self.maxPrice:
                    print('{} : Sending proposal of: {}'.format(self.public_key,newOffer))
                    proposal = Description({"price" : newOffer})
                    self.send_propose(msg_id+1, dialogue_id, origin, target+1, [proposal])
                    self.received_proposals.clear()
                else:
                    print('{} : Sending proposal of: {}'.format(self.public_key,self.maxPrice))
                    proposal = Description({"price" : self.maxPrice})
                    self.send_propose(msg_id+1, dialogue_id, origin, target+1, [proposal])
                    self.received_proposals.clear()

    def on_accept(self, msg_id: int, dialogue_id: int, origin: str, target: int):
        print('[{}] Our offer has been accepted!'.format(self.public_key))
        self.api.sync(self.api.tokens.transfer(self.account, Address(origin) , self.prevPrice, 20))
        print('Final Balance:', self.api.tokens.balance(self.account))

    def on_decline(self, msg_id: int, dialogue_id: int, origin: str, target: int) :
        print("[{}] Received a decline!".format(self.public_key))
        self.received_declines += 1

if __name__ == '__main__':

    #define the ledger parameters
    api = LedgerApi('127.0.0.1', 8100)

    #check if entity has already been created
    if(os.path.exists('./workdir/Agent_Auction/client/client_private.key')):

        #locate the agent account entity for interacting with the ledger.
        with open ('./workdir/Agent_Auction/client/client_private.key', 'r') as private_key_file:
                client_agentID = Entity.load(private_key_file)

    else:
        #create new entity for the agent
        client_agentID = Entity()
        #store private key of newly formed entity
        with open('./workdir/Agent_Auction/client/client_private.key', 'w') as private_key_file:
            client_agentID.dump(private_key_file)
        #give the account starting tokens
        api.sync(api.tokens.wealth(client_agentID, 1000))

    startBalance = api.tokens.balance(client_agentID)

    # define an OEF Agent
    client_agent = ClientAgent(str(Address(client_agentID)), 50, 5, client_agentID, oef_addr="127.0.0.1", oef_port=10000)

    print('Balance Before:', startBalance)

    # connect it to the OEF Node
    client_agent.connect()

    # query OEF for DataService providers
    echo_query1 = Query([Constraint("timezone", Eq(3)), Constraint("twentyfour", Eq(False))],TIME_AGENT())


    client_agent.search_services(0, echo_query1)
    client_agent.run()
