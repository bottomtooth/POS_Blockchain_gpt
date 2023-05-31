import hashlib
import json


class Block:
    def __init__(self, index, timestamp, transactions, proof, previous_hash, validator_address):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.proof = proof
        self.previous_hash = previous_hash
        self.validator_address = validator_address
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [str(tx) for tx in self.transactions],
            "proof": self.proof,
            "previous_hash": self.previous_hash,
            "validator_address": self.validator_address
        }
        data_string = json.dumps(data, sort_keys=True)
        return hashlib.sha3_256(data_string.encode()).hexdigest()

    

    def __str__(self):
        block_details = {
            "Index": self.index,
            "Timestamp": self.timestamp,
            "Transactions": self.transactions,
            "Proof": self.proof,
            "Previous Hash": self.previous_hash,
            "Validator Address": self.validator_address,
            "Hash": self.hash
        }
        return str(block_details)
