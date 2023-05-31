import hashlib
import json


def hash_transactions(transactions):
    if transactions:
        transaction_hashes = [hashlib.sha256(json.dumps(transaction).encode()).hexdigest() for transaction in transactions]
    else:
        transaction_hashes = [hashlib.sha256("".encode()).hexdigest()]
    return transaction_hashes


def merkle_tree(transaction_hashes):
    if len(transaction_hashes) == 1:  # If there's only one hash left, return it
        return transaction_hashes[0]
    elif len(transaction_hashes) % 2 != 0:  # If the number of hashes is odd, duplicate the last hash
        transaction_hashes.append(transaction_hashes[-1])
    new_transaction_hashes = []
    for i in range(0, len(transaction_hashes), 2):  # Pair the hashes and hash them together
        new_transaction_hashes.append(hashlib.sha256((transaction_hashes[i] + transaction_hashes[i+1]).encode()).hexdigest())
    return merkle_tree(new_transaction_hashes)  # Continue the process


def calculate_hash(index, timestamp, transactions, proof, previous_hash, validator_address):
    transaction_hashes = hash_transactions(transactions)
    merkle_root = merkle_tree(transaction_hashes)
    data = str(index) + str(timestamp) + merkle_root + str(proof) + str(previous_hash) + str(validator_address)
    return hashlib.sha256(data.encode()).hexdigest()
