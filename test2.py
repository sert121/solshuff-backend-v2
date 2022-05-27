import asyncio
from solana.rpc.async_api import AsyncClient
# from solana.keypair import Keypair
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.rpc.api import Client
from solana.system_program import TransferParams, transfer
from solana.transaction import Transaction
import ast

import os
from dotenv import load_dotenv
load_dotenv()
SEED_PRIV  = os.getenv("SEC")
SEED_PRIV = ast.literal_eval(SEED_PRIV)
print(SEED_PRIV,type(SEED_PRIV))



async def main():
# True
    # Alternatively, close the client explicitly instead of using a context manager:
    client = AsyncClient("https://api.devnet.solana.com")
    res = await client.is_connected()
    print(res)  # True
    
    sender, receiver = Keypair.from_seed(bytes(PublicKey(1))), Keypair.from_seed(bytes(PublicKey(2)))
    sender = Keypair.from_secret_key(bytes(SEED_PRIV))
    txn = Transaction().add(transfer(TransferParams(
        from_pubkey=sender.public_key, to_pubkey=receiver.public_key, lamports=1000)))

    res = await client.send_transaction(txn, sender)
    print(res)
    await client.close()
asyncio.run(main())