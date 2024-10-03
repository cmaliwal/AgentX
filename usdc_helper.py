from spl.token.constants import TOKEN_PROGRAM_ID
from spl.token.client import Token
from spl.token.instructions import get_associated_token_address
from solders.pubkey import Pubkey
import requests

# Constant for the USDC mint address on Solana
USDC_MINT_ADDRESS = "4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU"


def get_usdc_token_account(pubkey):
    mint_pubkey = Pubkey.from_string(USDC_MINT_ADDRESS)
    associated_token_account = get_associated_token_address(pubkey, mint_pubkey)
    return associated_token_account


def check_usdc_balance(client, pubkey):
    associated_token_account = get_usdc_token_account(Pubkey.from_string(pubkey))
    token = Token(client, Pubkey.from_string(USDC_MINT_ADDRESS), TOKEN_PROGRAM_ID, None)

    return token.get_balance(associated_token_account)


def transfer_usdc(client, sender_keypair, recipient_pubkey, amount):
    try:
        sender_pubkey = sender_keypair.pubkey()
        usdc_mint = Pubkey.from_string(USDC_MINT_ADDRESS)

        # Get associated token accounts for both sender and recipient
        sender_token_account = get_usdc_token_account(sender_pubkey)
        recipient_token_account = get_usdc_token_account(
            Pubkey.from_string(recipient_pubkey)
        )

        # Create a Token object for the USDC mint
        token = Token(client, usdc_mint, TOKEN_PROGRAM_ID, sender_keypair)

        # Transfer the USDC tokens (amount is converted to smallest unit, 10^6 for USDC)
        tx = token.transfer(
            source=sender_token_account,
            dest=recipient_token_account,
            owner=sender_keypair,
            amount=int(amount * 10**6),  # USDC has 6 decimal places
        )

        print(f"Transaction successful with signature: {tx}")
        return tx
    except Exception as e:
        print(f"Error transferring USDC: {e}")
        return None


def get_usdc_amount_for_sol(sol_amount):
    try:
        # Fetch SOL/USDC price from Binance API
        url = "https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDC"
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        sol_price = float(data["price"])

        # Calculate equivalent USDC amount
        return sol_amount * sol_price
    except requests.exceptions.RequestException as e:
        print(f"Error fetching SOL price: {e}")
        return None


# Example Usage (Commented out for reference)
# from solana.rpc.api import Client
# from wallet_utils import get_keypair_details

# client = Client("https://api.devnet.solana.com")

# Check USDC balance
# public_key = "FwVm7xKpqMCedbR24RYf227n1usXS1JzrTQikvve12Kz"
# usdc_balance = check_usdc_balance(client, public_key)
# print("USDC Balance:", usdc_balance)

# Get equivalent USDC amount for a given SOL amount
# usdc_amount = get_usdc_amount_for_sol(0.0001)
# print("Equivalent USDC:", usdc_amount)

# Transfer USDC
# secret_key = "49ZDbfbiWF4Vmqx7oTH8nxGv6vqGCm5bvDEHSvtuEW6cbuFF7MBW8cmgszq1PGzCGKJ27knU7mDkGcdEnSaK9sbe"
# sender = get_keypair_details(secret_key)
# recipient_pubkey = "2ZiqUxRQteU1sJPu1dgNU761RQme1vi5acseEUSHG8kL"
# transfer_usdc(client, sender["keypair"], recipient_pubkey, usdc_amount)
