from django import forms

class TransactionForm(forms.Form):
    sender = forms.CharField(label='Sender', max_length=100)
    recipient = forms.CharField(label='Recipient', max_length=100)
    amount = forms.DecimalField(label='Amount')

class ValidatorsForm(forms.Form):
    validator_name = forms.CharField(label='Validator Name')
    # Add more fields as needed
