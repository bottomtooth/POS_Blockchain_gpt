import hashlib
import json
import rsa

class Wallet:
    def __init__(self):
        self.public_key = None
        self.private_key = None

    def create_keys(self):
        (self.public_key, self.private_key) = rsa.newkeys(2048)

    def get_public_key(self):
        return self.public_key

    def get_private_key(self):
        return self.private_key

    def sign_transaction(self, transaction):
        transaction_data = json.dumps(transaction, sort_keys=True).encode()
        transaction_hash = hashlib.sha256(transaction_data).hexdigest()
        signature = rsa.sign(transaction_hash.encode(), self.private_key, 'SHA-256')
        return signature.hex()

    @staticmethod
    def verify_transaction(transaction):
        if 'sender' not in transaction or 'receiver' not in transaction or 'amount' not in transaction or 'signature' not in transaction:
            return False

        sender_public_key = rsa.PublicKey.load_pkcs1(transaction['sender'].encode())
        signature = bytes.fromhex(transaction['signature'])
        transaction_data = json.dumps(transaction, sort_keys=True).encode()
        return rsa.verify(transaction_data, signature, sender_public_key)
