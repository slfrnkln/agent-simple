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

#import logging
#from oef.logger import set_logger
#set_logger("oef.agents", logging.DEBUG)

def print_address_balances(api: LedgerApi, contract: SmartContract, addresses: [Address]):
    for idx, address in enumerate(addresses):
        print('Address{}: {:<6d} bFET {:<10d} TOK'.format(idx, api.tokens.balance(address), contract.query(api, 'balance', address=address)))
    print()

class Demo_Agent(OEFAgent):

    def __init__(self, public_key: str, oef_addr: str, oef_port: int = 10000):
        super().__init__(public_key, oef_addr, oef_port, loop=asyncio.new_event_loop())

        self.scheme = {}
        self.scheme['timezone'] = None
        self.scheme['id'] = None

    def on_cfp(self, msg_id: int, dialogue_id: int, origin: str, target: int, query: CFP_TYPES):
        """Send a simple Propose to the sender of the CFP."""
        print("[{0}]: Received CFP from {1}".format(self.public_key, origin))

        #data = self.get_latest(0)

        proposal = Description({"price" : price })
        print("[{0}]: Sending propose at price: {1}".format(self.public_key, price))
        self.send_propose(msg_id + 1, dialogue_id, origin, target + 1, [proposal])

    def on_accept(self, msg_id: int, dialogue_id: int, origin: str, target: int):
        """Once we received an Accept, send the requested data."""
        print("[{0}]: Received accept from {1}.".format(self.public_key, origin))

        api.sync(contract.action(api, 'transfer', fet_tx_fee, [server_agentID], Address(server_agentID), Address(origin), tok_transfer_amount))

        command = {}
        command["time"] = int(time.time())
        msg = json.dumps(command)
        self.send_message(0,dialogue_id, origin, msg.encode())

        print_address_balances(api, contract, [Address(server_agentID), Address(origin)])


    def on_decline(self, msg_id: int, dialogue_id: int, origin: str, target: int):
        print("declined")


    def on_message(self, msg_id: int, dialogue_id: int, origin: str, content: bytes):
        data = json.loads(content.decode())
        print ("message received: "  + json.dumps(data))


if __name__ == '__main__':


    with open ('./workdir/transfer2/server_private.key', 'r') as private_key_file:
        server_agentID = Entity.load(private_key_file)

    api = LedgerApi('127.0.0.1', 8100)
    price = ' 80 '
    tok_transfer_amount = 200
    fet_tx_fee = 40

    print('Starting Balance:', api.tokens.balance(server_agentID))

    with open ('./workdir/transfer2/agent/contract.one', 'r') as contract_file:
        contract = SmartContract.load(contract_file)

    print_address_balances(api, contract, [Address(server_agentID)])

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
