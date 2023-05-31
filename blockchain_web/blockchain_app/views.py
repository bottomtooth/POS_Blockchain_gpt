from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import TransactionForm, ValidatorsForm, RegistrationForm
from .models import Transaction, Block
from .Blockchain import Blockchain
from .Wallet import Wallet
from .Block import Block


# Create a global instance of the blockchain
validators = ["address1", "address2", "address3"]  # Replace with actual validator addresses
blockchain = Blockchain(validators)
wallet = Wallet()
# Create a wallet instance and generate keys
wallet.create_keys()


def index(request):
    chain_details = blockchain.get_chain()

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
            'amount': amount
        }
        blockchain.add_pending_transaction(transaction_data)

        # Redirect to the blockchain view after creating the transaction
        return redirect('view-blockchain')

    # Render the create transaction form
    return render(request, 'blockchain_app/create_transaction.html')


class CreateTransactionView(LoginRequiredMixin, FormView):
    template_name = 'blockchain_app/create_transaction.html'
    form_class = TransactionForm
    success_url = '/blockchain/'

    def form_valid(self, form):
        sender = form.cleaned_data['sender']
        recipient = form.cleaned_data['recipient']
        amount = form.cleaned_data['amount']

        latest_block = blockchain.get_last_block()
        transaction = Transaction(sender=sender, recipient=recipient, amount=amount)
        transaction.save()  # Save the transaction to get a transaction ID

        # Create a new block and assign it to the transaction
        block = Block.objects.create(index=latest_block.index + 1, timestamp=timezone.now(),
                                     previous_hash=latest_block.hash)
        transaction.block.add(block)  # Add the block to the transaction's many-to-many field

        return super().form_valid(form)


def mine(request):
    if request.method == 'POST':
        # Perform the mining process
        miner_address = request.POST['miner_address']
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


def manage_validators(request):
    form = ValidatorsForm()
    if request.method == 'POST':
        form = ValidatorsForm(request.POST)
        if form.is_valid():
            # Process the form data and perform necessary actions
            pass

    return render(request, 'blockchain_app/manage_validators.html', {'form': form})


def register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    form = AuthenticationForm(request, request.POST or None)
    if form.is_valid():
        login(request, form.get_user())
        return redirect('index')
    return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('index')  # Redirect to the home page after logout

