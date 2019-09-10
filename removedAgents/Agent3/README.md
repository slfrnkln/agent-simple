# Simple Negotiation Agent

Welcome to Fetch.AI Simple Agent repository. This is where you can see the most simple implementation of an Agent connecting to the OEF and making simple queries.
Simple Negotiation Agent has an addition to the protocol that on top of making queries will negotiate a price between the client and the data agent.
Once a deal is made, tokens will be transferred from one agent to the other followed by the exchange of data.
This will require the ledger set up and running in order to work.

## License

Fetch.AI Simple Agent is licensed under the Apache software license (see LICENSE file). Unless required by
applicable law or agreed to in writing, software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either \express or implied.

Fetch.AI makes no representation or guarantee that this software (including any third-party libraries)
will perform as intended or will be free of errors, bugs or faulty code. The software may fail which
could completely or partially limit functionality or compromise computer systems. If you use or
implement the ledger, you do so at your own risk. In no event will Fetch.AI be liable to any party
for any damages whatsoever, even if it had been advised of the possibility of damage.

As such this codebase should be treated as experimental and does not contain all currently developed
features. Fetch will be delivering regular updates.

## Supported platforms

* MacOS Darwin 10.13x and higher (64bit)
* Ubuntu 18.04 (x86_64)

(We plan to support all major platforms in the future)

## Getting Started with Trading

Following the README in the main folder you can follow these steps to get started with the simple trading agent.

Make sure the ledger and the oef is set up and running locally.

You can change the path in the Dockerfile or run the Simple Negotiation Agent with:

    python3 workdir/Agent3/agent/demo_agent.py

For the client, to interact with the Simple Negotiation Agent, run:

    python3 workdir/Agent3/client/client_agent.py

You may also like to see how the demo agent deals with multiple clientel with regards to negotiation.

You can test this by running the multiClient script here:

    python3 workdir/Agent3/client/multiClient.py
