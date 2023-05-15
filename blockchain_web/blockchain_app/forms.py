from django import forms

class TransactionForm(forms.Form):
    sender = forms.CharField(label='Sender', max_length=100)
    recipient = forms.CharField(label='Recipient', max_length=100)
    amount = forms.DecimalField(label='Amount')
