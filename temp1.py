from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.rpc.api import Client
from solana.system_program import TransferParams, transfer
from solana.transaction import Transaction


sender, receiver = Keypair.from_seed(bytes(PublicKey(1))), Keypair.from_seed(bytes(PublicKey(2)))
txn = Transaction().add(transfer(TransferParams(
    from_pubkey=sender.public_key, to_pubkey=receiver.public_key, lamports=1000)))
# solana_client = Client("http://localhost:8899")
solana_client.send_transaction(txn, sender)


{'jsonrpc': '2.0',
 'result': '236zSA5w4NaVuLXXHK1mqiBuBxkNBu84X6cfLBh1v6zjPrLfyECz4zdedofBaZFhs4gdwzSmij9VkaSo2tR5LTgG',
 'id': 12}
