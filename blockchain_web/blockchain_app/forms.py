from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class TransactionForm(forms.Form):
    sender = forms.CharField(label='Sender', max_length=100)
    recipient = forms.CharField(label='Recipient', max_length=100)
    amount = forms.DecimalField(label='Amount')

class ValidatorsForm(forms.Form):
    validator_name = forms.CharField(label='Validator Name')
    # Add more fields as needed
