from django.db import models
from django.contrib.auth.models import User


class Block(models.Model):
    index = models.PositiveIntegerField()
    timestamp = models.DateTimeField()
    previous_hash = models.CharField(max_length=64)
    nonce = models.PositiveIntegerField()
    hash = models.CharField(max_length=64)

    def __str__(self):
        return f"Block {self.index}"


class Transaction(models.Model):
    sender = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100, default='default_receiver')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField()
    block = models.ForeignKey(Block, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return f"Transaction from {self.sender} to {self.receiver}"


class Wallet(models.Model):
    public_key = models.CharField(max_length=256)
    private_key = models.CharField(max_length=256)

    def __str__(self):
        return f"Wallet with public key: {self.public_key}"
