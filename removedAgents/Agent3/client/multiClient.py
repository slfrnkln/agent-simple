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

import client_agent
from client_agent import ClientAgent



def makeClient(number: int):

    #check if entity has already been created
    if(os.path.exists('./workdir/Agent3/client/client'+str(number)+'_private.key')):

        #locate the agent account entity for interacting with the ledger.
        with open ('./workdir/Agent3/client/client'+str(number)+'_private.key', 'r') as private_key_file:
                client_agentID = Entity.load(private_key_file)

    else:
        #create new entity for the agent
        client_agentID = Entity()
        #store private key of newly formed entity
        with open('./workdir/Agent3/client/client'+str(number)+'_private.key', 'w') as private_key_file:
            client_agentID.dump(private_key_file)
        #give the account starting tokens
        api.sync(api.tokens.wealth(client_agentID, 2000))

    startBalance = api.tokens.balance(client_agentID)

    highest_price = random.randint(500, 1000)

    # define an OEF Agent
    client= ClientAgent(str(Address(client_agentID)), highest_price, client_agentID, oef_addr="127.0.0.1", oef_port=10000)

    print('Balance Before:', startBalance)

    # connect it to the OEF Node
    client.connect()

    # query OEF for DataService providers
    echo_query1 = Query([Constraint("timezone", Eq(3)), Constraint("twentyfour", Eq(False))],TIME_AGENT())


    client.search_services(0, echo_query1)
    client.run()

if __name__ == '__main__':
    #define the ledger parameters
    api = LedgerApi('127.0.0.1', 8100)

    for i in range(10):
        x = threading.Thread(target=makeClient, args=(i,))
        x.start()
