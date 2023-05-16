import time
import hashlib
import json
from .Block import Block
from .Wallet import Wallet


class Blockchain:
    def __init__(self, validators):
        self.chain = []
        self.pending_transactions = []
        self.validators = validators
        self.wallets = {}
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, time.strftime("%Y-%m-%d %H:%M:%S"), [], "Genesis", "Genesis", None)
        self.chain.append(genesis_block)

        # Generate wallet address and private key
        wallet = Wallet()
        wallet.create_keys()

        # Store the wallet address and private key securely
        self.wallets = {wallet.get_public_key(): wallet.get_private_key()}

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, block):
        self.chain.append(block)
        self.pending_transactions = []

    def add_pending_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def proof_of_work(self, previous_hash):
        nonce = 0
        while self.valid_proof(previous_hash, nonce) is False:
            nonce += 1
        return nonce

    def valid_proof(self, previous_hash, nonce):
        guess = f'{previous_hash}{nonce}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def mine_block(self, miner_address):
        if not self.chain:
            # Create a genesis block
            genesis_block = Block(0, time.strftime("%Y-%m-%d %H:%M:%S"), self.pending_transactions, "0", "0", miner_address)
            self.add_block(genesis_block)

            reward_transaction = {
                "sender": "blockchain",
                "recipient": miner_address,
                "amount": 1,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            self.add_pending_transaction(reward_transaction)

            print("Genesis block mined and added to the blockchain.")
            return

        previous_block = self.get_last_block()
        previous_hash = previous_block.calculate_hash()
        proof = self.proof_of_work(previous_hash)

        block = Block(len(self.chain), time.strftime("%Y-%m-%d %H:%M:%S"), self.pending_transactions, proof, previous_hash, miner_address)
        self.add_block(block)

        reward_transaction = {
            "sender": "blockchain",
            "recipient": miner_address,
            "amount": 1,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.add_pending_transaction(reward_transaction)

        print("Block mined and added to the blockchain.")

    def get_chain(self):
        chain_data = []
        for block in self.chain:
            chain_data.append(block.__dict__)
        return json.dumps({"chain": chain_data}, indent=4)

    def calculate_wallet_balance(self, wallet_address):
        balance = 0

        for block in self.chain:
            for transaction in block.transactions:
                if transaction['sender'] == wallet_address:
                    balance -= transaction['amount']
                if transaction['recipient'] == wallet_address:
                    balance += transaction['amount']

        return balance

    def __str__(self):
        return self.get_chain()
