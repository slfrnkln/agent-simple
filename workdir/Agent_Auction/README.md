# Simple Auction Agent

Welcome to Fetch.AI Simple Agent repository. This is where you can see the most simple implementation of an Agent connecting to the OEF and making simple queries.
The Simple Auction Agent uses a modified version of the FIPA English Auction Interaction Protocol to conduct an Auction for example data between multiple agents.
The auction continues through handling multiple agents until one participant outbids the rest to purchase the data. The winning client will then transfer the
bidded amount of tokens to recieve the example data.

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

Following the README in the main folder you can follow these steps to get started with the simple auction agent.

Make sure the ledger and the oef is set up and running locally.

To run the auction agent you can change the path in the Dockerfile or run the simple trading agent with:

    python3 workdir/Agent_Auction/agent/demo_agent.py

To run a participant there is an example client which you can run from here:

    python3 workdir/Agent_Auction/client/client_agent.py

For the full example run the multiClient script here:

    python3 workdir/transfer/client/client_agent.py

This script will create 10 participants with random max bid limits and bidding intervals, to interact with the auctioneer.
Whichever client out bids the others will win the auction, transfer tokens and recieve the data.
