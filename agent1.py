from typing import Dict, Any
from uagents import Agent, Context, Model
from solana.rpc.api import Client
from wallet_utils import derive_keypair_from_seed_phrase
from transaction_utils import get_sol_transfer_amount
from usdc_helper import get_usdc_amount_for_sol, transfer_usdc


# Seed phrase used to derive the wallet keypair for the agent
seed_phrase = ("<ENTER-SEED-PHRASE-HERE>")


# Define the request model for the swap order
class SwapOrderRequest(Model):
    from_agent: str  # Agent initiating the swap
    agent_owner: str  # The owner of the agent
    transaction_hash: str  # Transaction hash related to the swap


# Define the response model for the swap order
class SwapOrderResponse(Model):
    result: str  # The result of the swap process (e.g., transaction status)


# Initialize the agent with the name, port, and endpoint configuration
agent = Agent(
    name="Agent 1",
    port=8000,
    seed="Agent 1",
    endpoint=["http://127.0.0.1:8000/submit"],
)

# Solana client connected to the devnet
client = Client("https://api.devnet.solana.com")

# Create a wallet keypair from the seed phrase at derivation path index 0
wallet: Dict[str, Any] = derive_keypair_from_seed_phrase(seed_phrase, 0)


@agent.on_event("startup")
async def start_agent(ctx: Context):
    # Agent is initialized, log its address
    ctx.storage.set("orders", {})
    ctx.logger.info(f"Agent 1 initialized with address: {agent.address}")


# Handler for swap order messages
@agent.on_message(model=SwapOrderRequest, replies={SwapOrderResponse})
async def swap_request_handler(
    ctx: Context,
    sender: str,
    msg: SwapOrderRequest
):
    # Fetch orders from storage (presumed to be a dictionary)
    orders: Dict[str, Dict[str, Any]] = ctx.storage.get("orders")

    # Initialize sender and transaction hash in orders if not present
    if sender not in orders:
        orders[sender] = {}
    if msg.transaction_hash not in orders[sender]:
        orders[sender][msg.transaction_hash] = {
            "agent": msg.from_agent,
            "owner": msg.agent_owner,
            "completed": False,
        }

    # Log the received swap order message
    ctx.logger.info("Received Swap order message")

    # Get SOL transfer details based on the transaction hash
    try:
        (sent_by, received_by, amount) = get_sol_transfer_amount(
            client, msg.transaction_hash
        )
    except Exception as e:
        ctx.logger.error(f"Error fetching transfer amount: {e}")
        return SwapOrderResponse(result="Error in transfer")

    # Convert the SOL amount to USDC
    usdc_amount = get_usdc_amount_for_sol(amount)

    # Transfer the calculated USDC to the agent owner
    try:
        tx = transfer_usdc(
            client,
            wallet["keypair"],
            msg.agent_owner,
            usdc_amount
        )
    except Exception as e:
        ctx.logger.error(f"Error during USDC transfer: {e}")
        return SwapOrderResponse(result="Error in transfer")

    # If the transaction is successful, mark the order as completed
    if tx:
        orders[sender][msg.transaction_hash]["completed"] = True
        ctx.storage.set("orders", orders)

    # Return the transaction result as a response
    return SwapOrderResponse(result=str(tx))


# Main entry point to run the agent
if __name__ == "__main__":
    # Run the agent
    agent.run()
