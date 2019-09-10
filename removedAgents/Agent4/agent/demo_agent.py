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

import asyncio

import uuid
import time

class Demo_Agent(OEFAgent):

    def __init__(self, public_key: str, oef_addr: str, oef_port: int = 10000):
        super().__init__(public_key, oef_addr, oef_port, loop=asyncio.new_event_loop())

        self.scheme = {}
        self.scheme['timezone'] = None
        self.scheme['id'] = None

        self.cost = 0
        self.pending_cfp = 0
        self.received_proposals = []
        self.received_declines = 0

    def on_cfp(self, msg_id: int, dialogue_id: int, origin: str, target: int, query: CFP_TYPES):
        """Send a simple Propose to the sender of the CFP."""
        print("[{0}]: Received CFP from {1}".format(self.public_key, origin))

        #format the price for number extraction on other agent
        proposal = Description({"price" : wanted_price, "previous" : 0, "offer" : 0, "id" : 0})
        print("[{0}]: Sending propose at price: {1}".format(self.public_key, wanted_price))
        self.send_propose(msg_id + 1, dialogue_id, origin, target + 1, [proposal])
        startBalance = api.tokens.balance(server_agentID)

    def on_propose(self, msg_id: int, dialogue_id: int, origin: str, target: int, proposals: PROPOSE_TYPES):
        """When we receive a Propose message, check if we can afford the data. If so we accept, else we decline the proposal."""
        print("[{0}]: Received propose from agent {1}".format(self.public_key, origin))

        for i,p in enumerate(proposals):
            self.received_proposals.append({"agent" : origin,
                                            "proposal":p.values})

        received_cfp = len(self.received_proposals) + self.received_declines

        self.received_proposals.sort(key = lambda i: (i['proposal']['id']), reverse = True)

        print("I am here")
        if len( self.received_proposals) >= 1 :
            proposed = str(self.received_proposals[0]['proposal'])
            price = int(self.received_proposals[0]['proposal']['price'])
            offer = int(self.received_proposals[0]['proposal']['offer'])
            previous = int(self.received_proposals[0]['proposal']['previous'])
            proposalID = self.received_proposals[0]['proposal']['id']
            print('----->PRICE:', price)
            print('----->OFFER:', offer)
            print('----->PREVIOUS:', previous)
            print('----->ID:', proposalID)
            if price >= lowest_price:
                print('Good offer! Return offer and wait for accept...')
                proposal = Description({"price" : price, "previous": previous, "offer": price, "id": proposalID+1})
                print("[{0}]: Sending propose at price: {1}".format(self.public_key, price))
                self.send_propose(msg_id + 1, dialogue_id, origin, target + 1, [proposal])
            elif price == offer:
                print('Not going high enough. Ending dialogue')
                self.send_decline(msg_id,dialogue_id,self.received_proposals[0]['agent'],msg_id + 1)
                self.received_proposals = []
                return
            else:
                print('Too Low!')
                if ((price + previous)/2) >= lowest_price:
                    print('Ok, meet in the middle')
                    proposal = Description({"price" : ((price + previous)/2), "previous": previous, "offer": price, "id": proposalID+1})
                    print("[{0}]: Sending propose at price: {1}".format(self.public_key, ((price + previous)/2)))
                    self.send_propose(msg_id + 1, dialogue_id, origin, target + 1, [proposal])
                else:
                    print('Not Budging!')
                    currentOffer = price
                    proposal = Description({"price" : previous, "previous": previous, "offer": price, "id": proposalID+1})
                    print("[{0}]: Sending propose at price: {1}".format(self.public_key, previous))
                    self.send_propose(msg_id + 1, dialogue_id, origin, target + 1, [proposal])
        else:
            print("They don't have data")
            self.stop()

    def on_accept(self, msg_id: int, dialogue_id: int, origin: str, target: int):
        """Once we received an Accept, check the correct funds have been recieved. If so send the requested data."""
        print("[{0}]: Received accept from {1}.".format(self.public_key, origin))

        self.received_proposals = []

        if startBalance < api.tokens.balance(server_agentID):
            command = {}
            command["time"] = int(time.time())
            msg = json.dumps(command)
            self.send_message(0,dialogue_id, origin, msg.encode())

            print('Final Balance:', api.tokens.balance(server_agentID))
        else:
            print('No Funds Sent!')
            print('Ending Dialogue')
            return


    def on_decline(self, msg_id: int, dialogue_id: int, origin: str, target: int):
        print("declined")
        self.received_proposals = []


    def on_message(self, msg_id: int, dialogue_id: int, origin: str, content: bytes):
        data = json.loads(content.decode())
        print ("message received: "  + json.dumps(data))


if __name__ == '__main__':

    #define the ledger parameters
    api = LedgerApi('127.0.0.1', 8100)

    #checl if entity has already been generated
    if(os.path.exists('./workdir/Agent4/agent/server_private.key')):

        #locate the agent account entity for interacting with the ledger.
        with open ('./workdir/Agent4/agent/server_private.key', 'r') as private_key_file:
                server_agentID = Entity.load(private_key_file)

    else:
        #create the enity for the agent
        server_agentID = Entity()
        #store the private key of the newly created entity
        with open('./workdir/Agent4/agent/server_private.key', 'w') as private_key_file:
            server_agentID.dump(private_key_file)

    startBalance = api.tokens.balance(server_agentID)

    #set trading values
    wanted_price = 2000
    lowest_price = 1200

    fet_tx_fee = 40

    print('Wanted:', wanted_price)
    print('Lowest:', lowest_price)
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
