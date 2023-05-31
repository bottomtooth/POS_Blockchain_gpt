import hashlib
import json
import rsa
import secrets

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
import rsa


class Wallet:
    def __init__(self):
        self.public_key = None
        self.encrypted_private_key = None
        self.key = secrets.token_bytes(16)  # Use secrets module for generating the AES key

    def create_keys(self):
        (public_key, private_key) = rsa.newkeys(2048)
        self.public_key = public_key.save_pkcs1().decode()  # Convert to string
        self.encrypted_private_key = self.encrypt_private_key(private_key.save_pkcs1().decode())  # Convert to string

    def encrypt_private_key(self, private_key):
        cipher = AES.new(self.key, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(private_key.encode())
        return b64encode(nonce + tag + ciphertext).decode('utf-8')

    def decrypt_private_key(self):
        try:
            b64_decoded = b64decode(self.encrypted_private_key)
            nonce, tag, ciphertext = [b64_decoded[i : i + 16] for i in range(0, len(b64_decoded), 16)]
            cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
            decrypted_private_key = cipher.decrypt_and_verify(ciphertext, tag)
            return rsa.PrivateKey.load_pkcs1(decrypted_private_key)
        except Exception as e:
            print(f"Error decrypting private key: {e}")
            return None

    def sign_transaction(self, transaction):
        private_key = self.decrypt_private_key()
        if private_key is None:
            return None
        transaction_data = json.dumps(transaction, sort_keys=True).encode()
        transaction_hash = hashlib.sha256(transaction_data).hexdigest()
        signature = rsa.sign(transaction_hash.encode(), private_key, 'SHA-256')
        return signature.hex()

    def get_public_key(self):
        return self.public_key

    def get_private_key(self):
        return self.decrypt_private_key()

    @staticmethod
    def verify_transaction(transaction):
        if 'sender' not in transaction or 'receiver' not in transaction or 'amount' not in transaction or 'signature' not in transaction:
            return False

        sender_public_key = rsa.PublicKey.load_pkcs1(transaction['sender'].encode())
        signature = bytes.fromhex(transaction['signature'])
        transaction_data = json.dumps(transaction, sort_keys=True).encode()
        return rsa.verify(transaction_data, signature, sender_public_key)

    def calculate_balance(self, blockchain):
        balance = 0
        for block in blockchain.chain:
            for transaction in block.transactions:
                if transaction['recipient'] == self.public_key:
                    balance += transaction['amount']
                if transaction['sender'] == self.public_key:
                    balance -= transaction['amount']
        return balance
