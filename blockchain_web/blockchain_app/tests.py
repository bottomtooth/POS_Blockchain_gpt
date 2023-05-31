from django.test import TestCase

import unittest
from .Block import Block
from .Blockchain import Blockchain

class TestBlock(unittest.TestCase):
    def test_calculate_hash(self):
        block = Block(0, "2023-05-26 12:00:00", [], "Genesis", "Genesis", None)
        self.assertEqual(block.calculate_hash(), "expected_hash")

class TestBlockchain(unittest.TestCase):
    def setUp(self):
        self.blockchain = Blockchain(["validator1", "validator2", "validator3"])

    def test_create_genesis_block(self):
        self.assertEqual(len(self.blockchain.chain), 1)
        self.assertEqual(self.blockchain.chain[0].index, 0)
        self.assertEqual(self.blockchain.chain[0].proof, "Genesis")

    def test_add_block(self):
        block = Block(1, "2023-05-26 12:00:00", [], "proof", "previous_hash", "validator_address")
        self.blockchain.add_block(block)
        self.assertEqual(len(self.blockchain.chain), 2)
        self.assertEqual(self.blockchain.chain[1], block)

    # Add more tests as needed

if __name__ == "__main__":
    unittest.main()

