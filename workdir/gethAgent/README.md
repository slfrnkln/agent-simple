# Ethereum (Geth) Agent

Welcome to Fetch.AI Simple Agent repository. This is where you can see the most simple implementation of an Agent connecting to the OEF and making simple queries.
This particular agent is an example of one that can accept multiple cryptocurrencies. In this case the client agent can purchase the data for either (test) Ethereum
or (test) FET. It uses the same OEF framework as Agent2 with additional code to implement the Ethereum side. This guide will take you through setting up your own private
etherum node using Geth and how to begin trading with this agent.

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

## Getting Started with the Ethereum Agent

Following the README in the main folder you can follow these steps to get started with the simple trading agent.

Make sure the ledger and the oef is set up and running locally.

### Setting up the private Ethereum node (geth)

First you need to install [geth](https://geth.ethereum.org/install-and-build/Installing-Geth "Install Geth Here!") (Go Ethereum)

To check geth is installed correctly in the current directory run:

  $geth version

You should get a similar output to this:

  Geth
  Version: 1.9.2-stable
  Git Commit: e76047e9f5499b58064bddde514dd3119a090adf
  Architecture: amd64
  Protocol Versions: [63]
  Network Id: 1
  Go Version: go1.11.5
  Operating System: linux
  GOPATH=
  GOROOT=/usr/lib/go-1.11
