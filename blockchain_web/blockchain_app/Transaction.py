import ecdsa
from decimal import Decimal


class Transaction:
    def __init__(self, sender_address, sender_private_key, recipient_address, amount):
        self.sender_address = sender_address
        self.sender_private_key = sender_private_key
        self.recipient_address = recipient_address
        self.amount = amount

    def generate_signature(self):
        private_key = ecdsa.SigningKey.from_string(bytes.fromhex(self.sender_private_key), curve=ecdsa.SECP256k1)
        message = self.__str__().encode('utf-8')
        signature = private_key.sign(message)
        return signature.hex()

    def is_valid(self):
        if self.sender_address == self.recipient_address:
            return False

        if not isinstance(self.amount, Decimal) or self.amount <= 0:
            return False

        # Add more checks as needed

        public_key = ecdsa.VerifyingKey.from_string(bytes.fromhex(self.sender_address), curve=ecdsa.SECP256k1)
        signature = bytes.fromhex(self.signature)
        message = self.__str__().encode('utf-8')
        try:
            return public_key.verify(signature, message)
        except ecdsa.keys.BadSignatureError:
            return False

    def __str__(self):
        return f"{self.sender_address}->{self.recipient_address}: {self.amount}"
