import unittest
import random

from bazaar.offer import Item
from bazaar.locations.privatemarket import *

class TestGetOfferForItem(unittest.TestCase):

    def setUp(self):
        random.seed(9834298)

    def __sell(self, IQ, item, modifier=None):
        pm = PrivateMarket(IQ, [item], modifier)
        return pm.get_offer_for_item(item)

    def test_get_offer_for_item(self):
        """Regression test against known random seed."""
        i = Item(1000)
        self.assertEqual(int(self.__sell(8, i, None)), 0)
        self.assertEqual(int(self.__sell(14, i, None)), 0)
        self.assertEqual(int(self.__sell(16, i, None)), 700)
        self.assertEqual(int(self.__sell(18, i, None)), 600)
        self.assertEqual(int(self.__sell(20, i, None)), 1020)
        self.assertEqual(int(self.__sell(20, i, None)), 570)

class TestSellItems(unittest.TestCase):

    item = Item(1000)
    expected_offers = [0, 0, 650, 0, 580, 540, 0, 680, 0, 0, 560]

    def setUp(self):
        random.seed(923847923)
        self.pm = PrivateMarket(15, [self.item] * len(self.expected_offers))

    def test_baseline(self):
        """Validate expected results individually."""
        for expected in self.expected_offers:
            self.assertEqual(int(self.pm.get_offer_for_item(self.item)), expected)

    def test_sell_items(self):
        """Batch items using same random seed for same results."""
        offers = self.pm.get_daily_offers()
        self.assertListEqual([int(offer) for offer in offers], self.expected_offers)

