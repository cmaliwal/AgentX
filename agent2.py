from uagents import Agent, Context, Model
from wallet_utils import derive_keypair_from_seed_phrase, transfer_sol

# Define a seed phrase to derive the wallet keypair
seed_phrase = "<ENTER-SEED-PHRASE-HERE>"


# Define a model for the swap order request
class SwapOrderRequest(Model):
    from_agent: str         # Address of the agent initiating the request
    agent_owner: str        # Public key of the wallet initiating the swap
    transaction_hash: str   # Hash of the transaction representing the SOL transfer


# Define a model for the swap order response
class SwapOrderResponse(Model):
    result: str  # Result of the swap request (e.g., success or failure)


# Create an agent instance with a unique name, port, and endpoint
agent = Agent(
    name="Agent 2",
    port=8001,
    seed="Agent 2",  # Seed for the agent's wallet
    endpoint=["http://127.0.0.1:8001/submit"],  # Endpoint for communication
)

# Creating the wallet for the agent using the seed phrase
wallet = derive_keypair_from_seed_phrase(seed_phrase, 1)


# Event handler for agent startup
@agent.on_event("startup")
async def start_agent(ctx: Context):
    ctx.logger.info(f"Agent 2 initialized with address: {agent.address}")

    # Initialize storage for orders (if needed)
    ctx.storage.set("orders", {})

    # Input the amount of SOL to exchange for USDC
    amount = float(input("Enter the amount of SOL you want to exchange for USDC: "))

    # Re-derive the wallet keypair using the seed phrase
    wallet = derive_keypair_from_seed_phrase(seed_phrase, 1)

    # Transfer the specified amount of SOL and get the transaction hash
    transaction = transfer_sol(
        from_keypair=wallet["keypair"],
        to_pubkey_base58=wallet["public_key_base58"],
        amount_sol=amount
    )

    # Prepare the swap order request message with transaction details
    transaction_message = SwapOrderRequest(
        from_agent=agent.address,
        agent_owner=wallet["public_key_base58"],
        transaction_hash=transaction
    )

    # Send the swap order request to the designated destination agent
    await ctx.send(
        destination="agent1qv8cc32up2v58lvg9sz2u4hedd2wmflcymspeym5jlcdvpud0srsxn39vvf",
        message=transaction_message
    )


if __name__ == "__main__":
    # Run the agent
    agent.run()
