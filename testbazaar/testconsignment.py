import unittest
import random

from bazaar.offer import Item
from bazaar.locations.consignment import *

class TestGetPercent(unittest.TestCase):

    def test_3vIQ(self):
        """At this level, percent must always be 41-60."""
        for i in range(1000):
            self.assertTrue(41 <= get_percent(3) <= 60)

    def test_4vIQ(self):
        """At this level, percent must always be 51-70."""
        for i in range(1000):
            self.assertTrue(51 <= get_percent(4) <= 70)

    def test_5vIQ(self):
        """At this level, percent will always be 61-80."""
        for i in range(1000):
            self.assertTrue(61 <= get_percent(5) <= 80)


class TestBestOfferAt(unittest.TestCase):

    def setUp(self):
        random.seed(23984729)

    def test_best_offer_at(self):
        """Regression test against known random seed."""
        i = Item(1000)
        self.assertEqual(int(find_best_offer_at(3, 14, i, None)), 480)
        self.assertEqual(int(find_best_offer_at(5, 16, i, None)), 0)
        self.assertEqual(int(find_best_offer_at(3, 14, i, None)), 420)
        self.assertEqual(int(find_best_offer_at(5, 16, i, None)), 720)

    def test_modifier(self):
        """For same rolls as above, modify by +- 10%."""
        i = Item(1000)
        self.assertEqual(int(find_best_offer_at(3, 14, i, 10)), 528)
        self.assertEqual(int(find_best_offer_at(5, 16, i, None)), 0)
        self.assertEqual(int(find_best_offer_at(3, 14, i, -10)), 378)
        self.assertEqual(int(find_best_offer_at(5, 16, i, 0)), 720)

    def test_difficulty(self):
        """Verify difficulties stored only for valid offers."""
        i = Item(1000)
        self.assertEqual(find_best_offer_at(3, 14, i, None).difficulty, 3)
        self.assertEqual(find_best_offer_at(5, 16, i, None).difficulty, None)
        self.assertEqual(find_best_offer_at(3, 14, i, None).difficulty, 3)
        self.assertEqual(find_best_offer_at(5, 16, i, None).difficulty, 5)

    def test_item(self):
        """Verify item stored for all offers, valid or no."""
        i = Item(1000)
        self.assertEqual(find_best_offer_at(3, 14, i, None).item.value, 1000)
        self.assertEqual(find_best_offer_at(5, 16, i, None).item.value, 1000)
        self.assertEqual(find_best_offer_at(3, 14, i, None).item.value, 1000)
        self.assertEqual(find_best_offer_at(5, 16, i, None).item.value, 1000)


class TestConsignItem(unittest.TestCase):

    def setUp(self):
        random.seed(9834298)

    def test_consign_item(self):
        """Regression test against known random seed."""
        i = Item(1000)
        self.assertEqual(int(consign_item(8, i, None)), 0)
        self.assertEqual(int(consign_item(14, i, None)), 460)
        self.assertEqual(int(consign_item(16, i, None)), 660)
        self.assertEqual(int(consign_item(18, i, None)), 690)
        self.assertEqual(int(consign_item(20, i, None)), 600)
        self.assertEqual(int(consign_item(20, i, None)), 790)

    def test_final_difficulty(self):
        """Regression test against known random seed."""
        i = Item(1000)
        self.assertEqual(consign_item(8, i, None).difficulty, None)
        self.assertEqual(consign_item(14, i, None).difficulty, 3)
        self.assertEqual(consign_item(16, i, None).difficulty, 4)
        self.assertEqual(consign_item(18, i, None).difficulty, 5)
        self.assertEqual(consign_item(20, i, None).difficulty, 4)
        self.assertEqual(consign_item(20, i, None).difficulty, 6)

class TestConsignItems(unittest.TestCase):

    item = Item(1000)
    IQ = 12
    expected_offers = [500, 530, 540, 490, 570, 430, 700,
                       640, 430, 0, 520]

    def setUp(self):
        random.seed(839223902)

    def test_baseline(self):
        """Validate expected results individually."""
        for expected in self.expected_offers:
            self.assertEqual(int(consign_item(self.IQ, self.item, None)), expected)

    def test_consign_items(self):
        """Batch items using same random seed for same results."""
        offers = consign_items(self.IQ, [self.item] * len(self.expected_offers), None)
        self.assertListEqual([int(offer) for offer in offers], self.expected_offers)
