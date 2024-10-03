from base58 import b58decode
from solders.signature import Signature
from solders.pubkey import Pubkey


def get_sol_transfer_amount(client, transaction_hash):
    # Convert the transaction hash into a Signature object
    tx_signature = Signature.from_string(transaction_hash)

    # Fetch the transaction details from the Solana blockchain using the client
    transaction_response = client.get_transaction(tx_signature)

    # Extract the transaction object from the response
    transaction = transaction_response.value.transaction.transaction

    # Access the message and the instructions in the transaction
    transaction_messages = transaction.message
    transaction_instructions = transaction_messages.instructions

    # Extract the first instruction, assuming it's a SOL transfer
    instruction = transaction_instructions[0]

    # Get the index for the program_id
    program_id = instruction.program_id_index

    # Check if the instruction is a native SOL transfer
    if transaction_messages.account_keys[program_id] == Pubkey.from_string(
        "11111111111111111111111111111111"
    ):
        data = instruction.data

        # Ensure the data length is consistent with a SOL transfer (16 bytes)
        if len(data) == 16:
            # Retrieve sender and receiver public keys
            sender = transaction_messages.account_keys[instruction.accounts[0]]
            receiver = transaction_messages.account_keys[instruction.accounts[1]]

            # Decode the base58 encoded data and extract the lamports
            data_bytes = b58decode(data)
            lamports = int.from_bytes(data_bytes[-8:], "little")

            # Convert lamports to SOL (1 SOL = 1e9 lamports)
            amount = lamports / 1e9

            # Return the sender, receiver, and the amount of SOL transferred
            return sender, receiver, amount

    # If it's not a valid SOL transfer, return None
    return None


# Example Usage (Commented out)
# from solana.rpc.api import Client
# client = Client("https://api.devnet.solana.com")
# tx_hash = "5jBTL1iaDELJ8d2rpTMMX4VADGvKydNYKqHavE21hbVaxYSsP9qeBYL2EHuoeBKGaAtmp8hj3HsgZn3H8yqd36Aw"
# amount = get_sol_transfer_amount(client, tx_hash)
# print("Transferred amount:", amount)
