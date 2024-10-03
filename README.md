# AgentX

This project consists of two agents responsible for swapping SOL to USDC on the Solana blockchain. The first agent initiates the transfer of SOL, while the second agent calculates the equivalent USDC amount and handles the transfer to the specified wallet address.

## Overview

- **Agent 1**: Sends a specified amount of SOL based on a transaction input.
- **Agent 2**: Receives the transaction hash, calculates the corresponding USDC amount, and transfers it to the specified wallet address.

## Prerequisites

- Python 3.8 or higher
- Poetry for package management
- Access to the Solana devnet

## Installation

1. Clone the repository:

   ```bash
   git clone <REPOSITORY_URL>
   cd <REPOSITORY_NAME>
   ```

2. Install the required dependencies using Poetry:

   ```bash
   poetry install
   ```

3. Ensure you have the necessary environment variables set up (if required). For example, you may need to configure your seed phrase and other API credentials.

## Running the Agents

1. **Start Agent 1**: This agent is responsible for sending SOL.

   ```bash
   poetry run python agent1.py
   ```

2. **Start Agent 2**: After Agent 1 is running, start this agent to handle USDC calculations and transfers.

   ```bash
   poetry run python agent2.py
   ```

## Functionality

- **Agent 1** will wait for a user input of SOL amount and handle the transfer to a defined address. It will then log the transaction details.
  
- **Agent 2** will listen for incoming swap requests, fetch the transfer amount using the provided transaction hash, convert the SOL amount to USDC, and transfer the calculated amount to the wallet address specified in the swap order message.

## Dependencies

- `solders`: For working with keypairs and transactions.
- `solana`: Solana RPC API client for interacting with the Solana blockchain.
- `mnemonic`: For handling mnemonic seed phrases.
- `uagents`: For the agent framework used in the project.

## Example Usage

To perform a swap:

1. Start Agent 1 and input the SOL amount to send.
2. Agent 1 will process the transaction and log the transaction hash.
3. Agent 2 will listen for the transaction hash and process the swap by calculating and transferring the corresponding USDC amount.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the Solana community for the tools and documentation that made this project possible.
- Thanks to the maintainers of the libraries used in this project.
