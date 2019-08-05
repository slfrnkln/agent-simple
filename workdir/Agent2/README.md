# Simple Agent 2

Welcome to Fetch.AI Simple Agent repository. This is where you can see the most simple implementation of an Agent connecting to the OEF and making simple queries.
Simple Agent 2 has an addition to the protocol that on top of making queries will set a price and transfer tokens from one agent to the other. This will require
the ledger set up and running in order to work.

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

To run the server trading agent you can change the path in the Dockerfile or run the simple trading agent with:

    python3 workdir/transfer/agent/demo_agent.py

For the client, to interact with the simple trading agent, run:

    python3 workdir/transfer/client/client_agent.py
