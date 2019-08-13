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

import threading
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

        self.received_proposals = []

        self.price = 0
        self.timeout = 0
        self.auction = False
        self.highestbid = None
        self.participants = []

    def on_cfp(self, msg_id: int, dialogue_id: int, origin: str, target: int, query: CFP_TYPES):
        """Send a simple Propose to the sender of the CFP."""
        print("[{0}]: Received CFP from {1}".format(self.public_key, origin))

        price = self.price
        proposal = Description({"auction" : True, "price" : price})
        print("[{0}]: Sending propose at price: {1}".format(self.public_key, price))
        self.send_propose(msg_id + 1, dialogue_id, origin, target + 1, [proposal])
        if self.auction == False:
            x = threading.Timer(5, self.startAuction)
            x.start()
            self.auction = True

    def on_propose(self, msg_id: int, dialogue_id: int, origin: str, target: int, proposals: PROPOSE_TYPES):
        print("[{0}]: Received propose from agent {1}".format(self.public_key, origin))

        for i,p in enumerate(proposals):
            self.received_proposals.append({"agent" : origin,
                                            "proposal":p.values})

    def on_accept(self, msg_id: int, dialogue_id: int, origin: str, target: int):
        """Once we received an Accept, check the correct funds have been recieved. If so send the requested data."""
        print("[{0}]: Received accept from {1}.".format(self.public_key, origin))
        self.participants.append(origin)

    def on_decline(self, msg_id: int, dialogue_id: int, origin: str, target: int):
        print('received decline!')
        self.participants.remove(origin)

    def on_message(self, msg_id: int, dialogue_id: int, origin: str, content: bytes):
        data = json.loads(content.decode())
        print ("message received: "  + json.dumps(data))

    #auction handler
    def startAuction(self):
        msgPrice = str(self.price)
        notify = "Auction starting at price:{}".format(self.price)
        msg = json.dumps(notify)
        for agent in self.participants:
            print('Sending {0} to {1}'.format(notify, agent))
            self.send_message(0, 0, agent, msg.encode())
        self.mainAuction(0, 0, 0)

    def mainAuction(self, msg_id: int, dialogue_id: int, target: int):
        proposal = Description({"price" : self.price})
        for agent in self.participants:
            print('Sending Proposal at price:{0} to: {1}'.format(self.price, agent))
            self.send_propose(msg_id+1, dialogue_id, agent, target+1, [proposal])
        time.sleep(timeout)
        currentBids = self.received_proposals
        if len(currentBids) > 1:
            currentBids.sort(key = lambda i: (i['proposal']['price']), reverse = True)
            for p in currentBids:
                if p['proposal']['price'] <= self.price:
                    print('Removing: {}'.format(p['agent']))
                    self.send_decline(msg_id+2, dialogue_id, p['agent'], msg_id+1)
                    self.participants.remove(p['agent'])
            if len(currentBids) > 1:
                self.highestbid = currentBids[0]
                self.price = currentBids[0]['proposal']['price']
                print('Current Leader:', self.highestbid)
                self.received_proposals.clear()
                currentBids.clear()
                self.mainAuction(msg_id+1, dialogue_id, target+1)
            else:
                if self.highestbid == None:
                    self.highestbid = self.received_proposals[0]
                    self.price = self.received_proposals[0]['proposal']['price']
                self.send_accept(msg_id, dialogue_id, self.highestbid['agent'], msg_id+1)
                print('Accepting highest bid of {}'.format(self.price))
                time.sleep(10)
                print('transfer data!')
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
                #create contract/transfer funds
        else:
            if self.highestbid == None:
                self.highestbid = self.received_proposals[0]
                self.price = self.received_proposals[0]['proposal']['price']
            self.send_accept(msg_id, dialogue_id, self.highestbid['agent'], msg_id+1)
            print('Accepting highest bid of {}'.format(self.price))
            time.sleep(15)
            print('transfer data!')
            if startBalance < api.tokens.balance(server_agentID):
                command = {}
                command["time"] = int(time.time())
                msg = json.dumps(command)
                self.send_message(0,dialogue_id, self.highestbid['agent'], msg.encode())

                print('Final Balance:', api.tokens.balance(server_agentID))
            else:
                print('No Funds Sent!')
                print('Ending Dialogue')
                return
            #create contract/transfer funds


if __name__ == '__main__':

    #define the ledger parameters
    api = LedgerApi('127.0.0.1', 8100)

    #checl if entity has already been generated
    if(os.path.exists('./workdir/Agent_Auction/agent/server_private.key')):

        #locate the agent account entity for interacting with the ledger.
        with open ('./workdir/Agent_Auction/agent/server_private.key', 'r') as private_key_file:
                server_agentID = Entity.load(private_key_file)

    else:
        #create the enity for the agent
        server_agentID = Entity()
        #store the private key of the newly created entity
        with open('./workdir/Agent_Auction/agent/server_private.key', 'w') as private_key_file:
            server_agentID.dump(private_key_file)

    startBalance = api.tokens.balance(server_agentID)

    #set trading values
    price = 20
    fet_tx_fee = 40

    print('Price:', price)
    print('Balance Before:', startBalance)

    # create agent and connect it to OEF
    server_agent = Demo_Agent(str(Address(server_agentID)), oef_addr="127.0.0.1", oef_port=10000)
    server_agent.scheme['timezone'] = 3
    server_agent.scheme['id'] = str(uuid.uuid4())
    server_agent.scheme['twentyfour'] = False
    server_agent.price = price
    timeout = 2
    server_agent.connect()
    # register a service on the OEF
    server_agent.description = Description(server_agent.scheme, TIME_AGENT())
    server_agent.register_service(0,server_agent.description)
    server_agent.run()
