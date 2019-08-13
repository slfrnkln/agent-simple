# Simple Agents

Welcome to Fetch.AI Simple Agent repository. This is where you can see the most simple implementation of an Agent connecting to the OEF and making simple queries.
There are now muliple agent examples contained within the repo of increasing complexity and use. Examples now contain:
A Simple Agent showing connecting and interacting over the OEF.
A Simple Trading Agent which introduces the transfering of tokens using the Ledger.
A Negotiating agent which implements basic negotiation stratergies into the agents trying to get the best price for their data.
Finally the Auction agent shows a simple example of a modified FIPA English Auction Interaction Protocol for selling data to the highest bidding client.

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

## Getting Started

First of all both the OEF and Ledger are required to be running locally for the agents to work.
For Agent 2 you are also required to have the ledger python api installed.

You can find information on how to install the OEF [here](https://github.com/fetchai/oef-search-pluto "Install the OEF here!").

Information on how to get started with the fetch ledger can be found [here](https://docs.fetch.ai/getting-started/versions/ "Install the Ledger here!")

To install the ledger api for python visit [here](https://github.com/fetchai/ledger-api-py "Install the Ledger API for Python here!").

Install the requirements.txt

    pip3 install -r requirements.txt

You will find additional README files in the respective agent folders.
