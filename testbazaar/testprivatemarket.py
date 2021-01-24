import unittest
import random

from bazaar.offer import Item
from bazaar.locations.privatemarket import *

class TestSellItem(unittest.TestCase):

    def setUp(self):
        random.seed(9834298)

    def test_sell_item(self):
        """Regression test against known random seed."""
        i = Item(1000)
        self.assertEqual(int(sell_item(8, i, None)), 0)
        self.assertEqual(int(sell_item(14, i, None)), 0)
        self.assertEqual(int(sell_item(16, i, None)), 700)
        self.assertEqual(int(sell_item(18, i, None)), 600)
        self.assertEqual(int(sell_item(20, i, None)), 1020)
        self.assertEqual(int(sell_item(20, i, None)), 570)

class TestSellItems(unittest.TestCase):

    item = Item(1000)
    IQ = 15
    expected_offers = [0, 0, 650, 0, 580, 540, 0, 680, 0, 0, 560]

    def setUp(self):
        random.seed(923847923)

    def test_baseline(self):
        """Validate expected results individually."""
        for expected in self.expected_offers:
            self.assertEqual(int(sell_item(self.IQ, self.item, None)), expected)

    def test_sell_items(self):
        """Batch items using same random seed for same results."""
        offers = sell_items(self.IQ, [self.item] * len(self.expected_offers), None)
        self.assertListEqual([int(offer) for offer in offers], self.expected_offers)

