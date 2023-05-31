from django.db import models
from django.contrib.auth.models import User


from django.db import models


class Block(models.Model):
    index = models.PositiveIntegerField()
    timestamp = models.DateTimeField()
    previous_hash = models.CharField(max_length=64)
    nonce = models.PositiveIntegerField()
    hash = models.CharField(max_length=64)
    transactions = models.ManyToManyField('Transaction', related_name='blocks')

    objects = models.Manager()  # Add this line to define the manager

    def save(self, *args, **kwargs):
        super(Block, self).save(*args, **kwargs)

    def __str__(self):
        return f"Block {self.index}"




class Transaction(models.Model):
    # sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transactions')
    # recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_transactions')

    sender = models.CharField(max_length=255)
    recipient = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    block = models.ManyToManyField(Block, related_name='transaction')

    def __str__(self):
        return f"Transaction(sender={self.sender}, recipient={self.recipient}, amount={self.amount})"


class Wallet(models.Model):

    public_key = models.CharField(max_length=256)
    private_key = models.CharField(max_length=256)

    objects = models.Manager()  # Add this line to define the manager

    def __str__(self):
        return f"Wallet with public key: {self.public_key}"

