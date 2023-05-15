from django.shortcuts import render, redirect
from .Blockchain import Blockchain
from django.http import HttpResponse
from .Wallet import Wallet
# Create a global instance of the blockchain
validators = ["address1", "address2", "address3"]  # Replace with actual validator addresses
blockchain = Blockchain(validators)
wallet = Wallet()
# Create a wallet instance and generate keys
wallet.create_keys()


def index(request):
    chain_details = blockchain.get_chain()

    # Create a wallet instance and generate keys
    wallet.create_keys()

    # Add public key to context dictionary
    context = {'chain_details': chain_details, 'public_key': wallet.get_public_key()}

    # Render the template with the blockchain data and public key
    return render(request, 'blockchain_app/index.html', context)


def view_blockchain(request):
    chain_details = blockchain.get_chain()
    return render(request, 'blockchain_app/view_blockchain.html', {'chain_details': chain_details})


def create_transaction(request):
    if request.method == 'POST':
        # Process the form data and create a new transaction
        sender = request.POST['sender']
        recipient = request.POST['recipient']
        amount = request.POST['amount']

        # Perform transaction validation and add to the blockchain
        transaction_data = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'signature': None  # Placeholder
        }
        blockchain.add_pending_transaction(transaction_data)

        # Redirect to the blockchain view after creating the transaction
        return redirect('view-blockchain')

    # Render the create transaction form
    return render(request, 'blockchain_app/create_transaction.html')

def mine(request):
    if request.method == 'POST':
        # Perform the mining process
        miner_address = 'your_miner_address'  # Replace with your miner address
        blockchain.mine_block(miner_address)

        # Redirect to the blockchain view after mining
        return redirect('view-blockchain')

    # Render the mine block form
    return render(request, 'blockchain_app/mine_block.html')


def view_last_block(request):
    last_block = blockchain.get_last_block()
    if last_block:
        block_details = last_block.get_block_details()
        return HttpResponse(f"Last Block: {block_details}")
    else:
        return HttpResponse("Blockchain is empty. No blocks to display.")


def view_wallet(request):
    public_key = request.GET.get('public_key')
    balance = blockchain.calculate_wallet_balance(public_key)  # Implement the balance calculation logic in the Blockchain class

    return render(request, 'blockchain_app/view_wallet.html', {'public_key': public_key, 'balance': balance})

