import hashlib


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
        data = str(self.index) + str(self.timestamp) + str(self.transactions) + str(self.proof) + str(self.previous_hash) + str(self.validator_address)
        return hashlib.sha256(data.encode()).hexdigest()

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
