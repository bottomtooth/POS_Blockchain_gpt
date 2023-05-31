from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Transaction


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class TransactionForm(forms.Form):
    sender = forms.CharField(max_length=100)
    recipient = forms.CharField(max_length=100)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError("The amount must be positive.")
        return amount

    def clean_sender(self):
        sender = self.cleaned_data['sender']
        if not self.is_valid_address(sender):
            raise forms.ValidationError("Invalid sender address.")
        return sender

    def clean_recipient(self):
        recipient = self.cleaned_data['recipient']
        if not self.is_valid_address(recipient):
            raise forms.ValidationError("Invalid recipient address.")
        return recipient

    def is_valid_address(self, address):
        # Implement your address validation logic here
        pass

    class Meta:
        model = Transaction
        fields = ['sender', 'recipient', 'amount']


class ValidatorsForm(forms.Form):
    validator_name = forms.CharField(label='Validator Name')
    # Add more fields as needed
