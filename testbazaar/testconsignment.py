import unittest
import random

from bazaar.offer import Item
from bazaar.locations.consignment import *

class TestGetPercent(unittest.TestCase):

    def test_3vIQ(self):
        """At this level, percent must always be 41-60."""
        for i in range(1000):
            self.assertTrue(41 <= Consignment._get_percent(None, 3) <= 60)

    def test_4vIQ(self):
        """At this level, percent must always be 51-70."""
        for i in range(1000):
            self.assertTrue(51 <= Consignment._get_percent(None, 4) <= 70)

    def test_5vIQ(self):
        """At this level, percent will always be 61-80."""
        for i in range(1000):
            self.assertTrue(61 <= Consignment._get_percent(None, 5) <= 80)


class TestFindBestOfferAt(unittest.TestCase):

    def setUp(self):
        random.seed(23984729)

    def __best_at(self, difficulty, IQ, item, modifier=None):
        c = Consignment(IQ, [item], modifier)
        return c._find_best_offer_at(difficulty, item)

    def test_best_offer_at(self):
        """Regression test against known random seed."""
        i = Item(1000)
        self.assertEqual(480, int(self.__best_at(3, 14, i, None)))
        self.assertEqual(  0, int(self.__best_at(5, 16, i, None)))
        self.assertEqual(420, int(self.__best_at(3, 14, i, None)))
        self.assertEqual(720, int(self.__best_at(5, 16, i, None)))

    def test_modifier(self):
        """For same rolls as above, modify by +- 10%."""
        i = Item(1000)
        self.assertEqual(528, int(self.__best_at(3, 14, i, 10)))
        self.assertEqual(  0, int(self.__best_at(5, 16, i, None)))
        self.assertEqual(378, int(self.__best_at(3, 14, i, -10)))
        self.assertEqual(720, int(self.__best_at(5, 16, i, 0)))

    def test_difficulty(self):
        """Verify difficulties stored only for valid offers."""
        i = Item(1000)
        self.assertEqual(self.__best_at(3, 14, i, None).difficulty, 3)
        self.assertEqual(self.__best_at(5, 16, i, None).difficulty, None)
        self.assertEqual(self.__best_at(3, 14, i, None).difficulty, 3)
        self.assertEqual(self.__best_at(5, 16, i, None).difficulty, 5)

    def test_item(self):
        """Verify item stored for all offers, valid or no."""
        i = Item(1000)
        self.assertEqual(self.__best_at(3, 14, i, None).item.value, 1000)
        self.assertEqual(self.__best_at(5, 16, i, None).item.value, 1000)
        self.assertEqual(self.__best_at(3, 14, i, None).item.value, 1000)
        self.assertEqual(self.__best_at(5, 16, i, None).item.value, 1000)


class TestGetOfferForItem(unittest.TestCase):

    def setUp(self):
        random.seed(9834298)

    def __offer(self, IQ, item, modifier=None):
        c = Consignment(IQ, [item], modifier)
        return c.get_offer_for_item(item)

    def test_consign_item(self):
        """Regression test against known random seed."""
        i = Item(1000)
        self.assertEqual(int(self.__offer(8, i, None)), 0)
        self.assertEqual(int(self.__offer(14, i, None)), 460)
        self.assertEqual(int(self.__offer(16, i, None)), 660)
        self.assertEqual(int(self.__offer(18, i, None)), 690)
        self.assertEqual(int(self.__offer(20, i, None)), 600)
        self.assertEqual(int(self.__offer(20, i, None)), 790)

    def test_final_difficulty(self):
        """Regression test against known random seed."""
        i = Item(1000)
        self.assertEqual(self.__offer(8, i, None).difficulty, None)
        self.assertEqual(self.__offer(14, i, None).difficulty, 3)
        self.assertEqual(self.__offer(16, i, None).difficulty, 4)
        self.assertEqual(self.__offer(18, i, None).difficulty, 5)
        self.assertEqual(self.__offer(20, i, None).difficulty, 4)
        self.assertEqual(self.__offer(20, i, None).difficulty, 6)

class TestGetDailyOffers(unittest.TestCase):

    item = Item(1000)
    expected_offers = [500, 530, 540, 490, 570, 430, 700,
                       640, 430, 0, 520]

    def setUp(self):
        random.seed(839223902)
        self.consign = Consignment(12, [self.item] * len(self.expected_offers))

    def test_baseline(self):
        """Validate expected results individually."""
        for expected in self.expected_offers:
            self.assertEqual(int(self.consign.get_offer_for_item(self.item)), expected)

    def test_consign_items(self):
        """Batch items using same random seed for same results."""
        offers = self.consign.get_daily_offers()
        self.assertListEqual([int(offer) for offer in offers], self.expected_offers)
