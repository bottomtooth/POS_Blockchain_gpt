from django.shortcuts import render, redirect
from .Blockchain import Blockchain
from django.http import HttpResponse
from .Wallet import Wallet
from .forms import ValidatorsForm, RegistrationForm
from .models import Transaction, Block
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create a global instance of the blockchain
validators = ["address1", "address2", "address3"]  # Replace with actual validator addresses
blockchain = Blockchain(validators)
wallet = Wallet()
# Create a wallet instance and generate keys
wallet.create_keys()


def index(request):
    chain_details = blockchain.get_chain()

    # Create a wallet instance and generate keys
    #wallet.create_keys()

    # Add public key to context dictionary
    context = {'chain_details': chain_details, 'public_key': wallet.get_public_key()}

    # Render the template with the blockchain data and public key
    return render(request, 'blockchain_app/index.html', context)


def view_blockchain(request):
    chain_details = blockchain.get_chain()
    return render(request, 'blockchain_app/view_blockchain.html', {'chain_details': chain_details})


def create_transaction(request):
    if request.method == 'POST':
        sender_username = request.POST['sender']
        recipient_username = request.POST['recipient']
        amount = request.POST['amount']

        try:
            sender = User.objects.get(username=sender_username)
            recipient = User.objects.get(username=recipient_username)

            transaction = Transaction(sender=sender, recipient=recipient, amount=amount)
            transaction.save()

            return redirect('view-blockchain')

        except User.DoesNotExist:
            # Handle the case when the user does not exist
            return HttpResponse('Invalid user')

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


def manage_validators(request):
    form = ValidatorsForm()
    if request.method == 'POST':
        form = ValidatorsForm(request.POST)
        if form.is_valid():
            # Process the form data and perform necessary actions
            # Retrieve the form field values using form.cleaned_data
            # Add the new validator to the blockchain or perform other operations
            # Redirect or display success message
            pass

    context = {
        'form': form,
    }
    return render(request, 'blockchain_app/manage_validators.html', context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to the home page after successful login
        else:
            error_message = 'Invalid username or password'
    else:
        error_message = ''
    return render(request, 'registration/login.html', {'error_message': error_message})


def user_logout(request):
    logout(request)
    return redirect('index')  # Redirect to the home page after logout

