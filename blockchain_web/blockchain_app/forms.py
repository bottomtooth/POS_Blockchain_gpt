from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Transaction


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['sender', 'recipient', 'amount']


class ValidatorsForm(forms.Form):
    validator_name = forms.CharField(label='Validator Name')
    # Add more fields as needed
