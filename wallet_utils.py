import base58
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import Transaction
from solders.system_program import TransferParams, transfer
from solana.rpc.api import Client
from solana.rpc.types import TxOpts
from mnemonic import Mnemonic
import json

# Initialize Mnemonic generator
mnemo = Mnemonic("english")

# Solana Devnet client instance
client = Client("https://api.devnet.solana.com")


def derive_keypair_from_seed_phrase(seed_phrase: str, account_index: int = 0):
    seed = mnemo.to_seed(seed_phrase)

    path = f"m/44'/501'/{account_index}'/0'"  # Derivation path for Solana wallets
    private_key = Keypair.from_seed_and_derivation_path(seed, path)

    keypair = Keypair.from_bytes(private_key.to_bytes_array())
    return {
        "keypair": keypair,
        "public_key": keypair.pubkey(),
        "public_key_base58": str(keypair.pubkey()),
        "private_key_bytes": keypair.secret(),
        "private_key_base58": base58.b58encode(keypair.secret()).decode(),
    }


def get_keypair_details(secret_key):
    keypair = Keypair.from_base58_string(secret_key)
    secret_key_bytes = keypair.secret()

    return {
        "keypair": keypair,
        "public_key": keypair.pubkey(),
        "public_key_base58": str(keypair.pubkey()),
        "private_key_bytes": secret_key_bytes,
        "private_key_base58": base58.b58encode(secret_key_bytes).decode(),
    }


def check_balance(pubkey):
    balance_resp = client.get_balance(Pubkey.from_bytes(bytes(pubkey)))
    balance = balance_resp.value
    return balance / 1_000_000_000  # Convert lamports to SOL


def transfer_sol(from_keypair, to_pubkey_base58, amount_sol):
    lamports = int(amount_sol * 1_000_000_000)  # Convert SOL to lamports
    to_pubkey = Pubkey.from_string(to_pubkey_base58)

    # Fetch the latest blockhash for transaction signing
    blockhash_resp = client.get_latest_blockhash()
    recent_blockhash = blockhash_resp.value.blockhash

    # Create transfer instruction
    transfer_instruction = transfer(
        TransferParams(
            from_pubkey=from_keypair.pubkey(), to_pubkey=to_pubkey, lamports=lamports
        )
    )

    # Create and sign the transaction
    transaction = Transaction.new_signed_with_payer(
        [transfer_instruction], from_keypair.pubkey(), [from_keypair], recent_blockhash
    )

    # Send the transaction and return the result
    response = json.loads(
        client.send_raw_transaction(
            bytes(transaction), opts=TxOpts(skip_confirmation=False)
        ).to_json()
    )

    return response["result"]


# Example usage (Commented out for reference):
# Example secret key (base58-encoded) for testing
# secret_key = "49ZDbfbiWF4Vmqx7oTH8nxGv6vqGCm5bvDEHSvtuEW6cbuFF7MBW8cmgszq1PGzCGKJ27knU7mDkGcdEnSaK9sbe"

# Example seed phrase used for deriving keypairs
# seed_phrase = (
#     "insane flee match effort slow husband market arrow sadness flame fish curious"
# )

# keypair_details = get_keypair_details(secret_key)
# sol_balance = check_balance(keypair_details["public_key"])
# seed_phrase_key_pair_details = derive_keypair_from_seed_phrase(seed_phrase, 1)
# sol_balance = check_balance(seed_phrase_key_pair_details["public_key"])
# transfer_transaction_signature = transfer_sol(seed_phrase_key_pair_details["keypair"], "FwVm7xKpqMCedbR24RYf227n1usXS1JzrTQikvve12Kz", 0.00000001)

# print(keypair_details)
# print(sol_balance)
# print(seed_phrase_key_pair_details)
# print(transfer_transaction_signature)
