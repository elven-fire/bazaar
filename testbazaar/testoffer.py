import unittest

from bazaar import BazaarError
from bazaar.offer import *

class TestItem(unittest.TestCase):

    def test_item(self):
        """Verify simple attribute storage."""
        i = Item(3000, "Sword of Hacking")
        self.assertEqual(i.value, 3000)
        self.assertEqual(i.name, "Sword of Hacking")

    def test_nonpositive_value(self):
        """Verify error on nonpositive value."""
        self.assertRaises(ItemError, Item, 0)
        self.assertRaises(ItemError, Item, -1000, "Sword")
        self.assertRaises(ValueError, Item, "Sword of Hacking")

    def test_name(self):
        """Verify unknown item name."""
        i = Item(3000)
        self.assertEqual(i.value, 3000)
        self.assertEqual(i.name, "Item valued at $3000")

    def test_str(self):
        """Verify string treatment as name."""
        self.assertEqual(str(Item(3000, "Sword of Hacking")), "Sword of Hacking")
        self.assertEqual(str(Item(3000)), "Item valued at $3000")

class TestOffer(unittest.TestCase):

    def test_offer(self):
        """Verify simple attribute storage."""
        o = Offer(Item(3000), 1500, 3)
        self.assertEqual(o.item.value, 3000)
        self.assertEqual(o.offer, 1500)
        self.assertEqual(o.difficulty, 3)
    
    def test_invalid_item(self):
        """Verify error on invalid item."""
        self.assertRaises(OfferError, Offer, "Sword", 1500)
        self.assertRaises(OfferError, Offer, 3000, 1500)
        
    def test_boolean(self):
        """Test offer treated as boolean by offer's existence."""
        i = Item(3000)
        self.assertTrue(Offer(i, 6000))
        self.assertTrue(Offer(i, 3000))
        self.assertTrue(Offer(i, 1000))
        self.assertFalse(Offer(i, 0))
        self.assertFalse(Offer(i, -3000))
        self.assertFalse(Offer(i, None))
        self.assertFalse(Offer(i))

    def test_int(self):
        """Test offer treated as int by actual offer price."""
        i = Item(3000)
        self.assertEqual(int(Offer(i, 500)), 500)
        self.assertEqual(int(NoOffer(i)), 0)

    def test_str(self):
        """Verify string treatment including item and offer value."""
        named_item = Item(3000, "Sword of Hacking")
        unnamed_item = Item(3000)
        self.assertEqual(str(Offer(named_item, 500)), "Sword of Hacking: offering $500 (16%)")
        self.assertEqual(str(Offer(unnamed_item, 2500)), "Item valued at $3000: offering $2500 (83%)")
        self.assertEqual(str(NoOffer(named_item)), "Sword of Hacking: No Offer")
        self.assertEqual(str(NoOffer(unnamed_item)), "Item valued at $3000: No Offer")

    def test_no_offer(self):
        """Test convenience function for a non-offer."""
        o = NoOffer(Item(3000))
        self.assertEqual(o.item.value, 3000)
        self.assertIsNone(o.offer)
        self.assertFalse(o)
