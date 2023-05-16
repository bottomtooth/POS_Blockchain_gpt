import time
from .Blockchain import Blockchain
from .Wallet import Wallet


class Node:
    def __init__(self):
        self.validators = ["validator1", "validator2", "validator3"]  # Update with your own list of validators
        self.blockchain = Blockchain(self.validators)
        self.wallet = Wallet()

    def run(self):
        while True:
            print("======= PoS Blockchain =======")
            print("1. Mine a new block")
            print("2. View the last block")
            print("3. View the blockchain")
            print("4. Create a new transaction")
            print("5. Exit")

            choice = input("Enter your choice: ")
            if choice == "1":
                self.mine()
            elif choice == "2":
                self.view_last_block()
            elif choice == "3":
                self.view_blockchain()
            elif choice == "4":
                self.create_transaction()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")

    def mine(self):
        miner_address = self.wallet.public_key
        self.blockchain.mine_block(miner_address)

    def view_last_block(self):
        last_block = self.blockchain.get_last_block()
        if last_block:
            print("Last Block:")
            print(last_block)
        else:
            print("Blockchain is empty. No blocks to display.")

    def view_blockchain(self):
        print("Blockchain:")
        print(self.blockchain)

    def create_transaction(self):
        sender = input("Sender: ")
        receiver = input("Receiver: ")
        amount = float(input("Amount: "))

        transaction = {
            "sender": sender,
            "recipient": receiver,
            "amount": amount,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        if self.wallet.sign_transaction(transaction):
            self.blockchain.add_pending_transaction(transaction)
            print("Transaction added to the pending transactions.")
        else:
            print("Transaction signature failed. Transaction not added.")

if __name__ == "__main__":
    node = Node()
    node.run()
