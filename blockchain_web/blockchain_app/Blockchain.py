import time
import hashlib
import json
import secrets
from .Block import Block
from .Wallet import Wallet


class Blockchain:
    def __init__(self, validators):
        self.chain = []
        self.pending_transactions = []
        self.validators = validators
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, time.strftime("%Y-%m-%d %H:%M:%S"), [], "Genesis", "Genesis", None)
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, block):
        if not block.is_valid():  # You'll need to implement this method
            raise ValueError("Invalid block")
        self.chain.append(block)
        self.pending_transactions = []

    def is_valid_block(self, block):
        # Implement your block validation logic here
        pass

    def validate_transaction(self, transaction):
        # Check that the transaction is well-formed
        if 'sender' not in transaction or 'recipient' not in transaction or 'amount' not in transaction:
            return False

        # Verify the transaction's signature
        if not Wallet.verify_transaction(transaction):  # You'll need to implement this method in the Wallet class
            return False

        # Check the sender's balance
        sender_balance = Wallet.calculate_balance(transaction['sender'])  # You'll need to implement this method
        if sender_balance < transaction['amount']:
            return False

        return True

    def add_pending_transaction(self, transaction):
        if self.validate_transaction(transaction):  # You'll need to implement this method
            self.pending_transactions.append(transaction)
            self.pending_transactions.sort(key=lambda tx: tx['fee'], reverse=True)  # Sort by fee, highest first
            print("Transaction added to the pending transactions.")
        else:
            print("Invalid transaction. Not added to the pending transactions.")

    def replace_pending_transaction(self, old_transaction, new_transaction):
        if self.validate_transaction(new_transaction):  # You'll need to implement this method
            self.pending_transactions.remove(old_transaction)
            self.pending_transactions.append(new_transaction)
            self.pending_transactions.sort(key=lambda tx: tx['fee'], reverse=True)  # Sort by fee, highest first
            print("Transaction replaced in the pending transactions.")
        else:
            print("Invalid transaction. Not replaced in the pending transactions.")

    def proof_of_work(self, previous_hash):
        nonce = secrets.randbelow(1000000)  # Generate a random number between 0 and 1000000
        while self.valid_proof(previous_hash, nonce) is False:
            nonce = secrets.randbelow(1000000)
        return nonce

    def valid_proof(self, previous_hash, nonce):
        guess = f'{previous_hash}{nonce}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:5] == "00000"  # Increase the number of zeros

    def mine_block(self, miner_address):
        if not self.chain:
            # Create a genesis block
            genesis_block = Block(0, time.strftime("%Y-%m-%d %H:%M:%S"), self.pending_transactions, "0", "0", miner_address)
            self.add_block(genesis_block)

            reward_transaction = {
                "sender": "Mining Reward",
                "recipient": miner_address,
                "amount": 1,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            #self.add_pending_transaction(reward_transaction)

            print("Genesis block mined and added to the blockchain.")
            return

        previous_block = self.get_last_block()
        previous_hash = previous_block.calculate_hash()
        proof = self.proof_of_work(previous_hash)

        block = Block(len(self.chain), time.strftime("%Y-%m-%d %H:%M:%S"), self.pending_transactions, proof, previous_hash, miner_address)
        self.add_block(block)

        reward_transaction = {
            "sender": "Mining Reward",
            "recipient": miner_address,
            "amount": 1,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.add_pending_transaction(reward_transaction)

        print("Block mined and added to the blockchain.")

        if not block.is_valid():  # You'll need to implement this method
            raise ValueError("Block mining failed")
        self.add_block(block)

    def get_chain(self):
        chain_data = []
        for block in self.chain:
            chain_data.append(block.__dict__)
        return json.dumps({"chain": chain_data}, indent=4)

    def resolve_conflicts(self, other_chain):
        if len(other_chain) > len(self.chain):
            self.chain = other_chain

    def __str__(self):
        return self.get_chain()
