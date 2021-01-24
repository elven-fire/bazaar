from bazaar import BazaarError

class ItemError(BazaarError):
    pass

class OfferError(BazaarError):
    pass

class Item:

    """An item available for sale."""

    def __init__(self, value, name=None):
        self.value = int(value)
        if self.value <= 0:
            raise ItemError("Invalid item value: %s" % self.value)
        self.name = name
        if self.name is None:
            self.name = "Item valued at $%d" % self.value

    def __str__(self):
        """Return name of item."""
        return self.name

class Offer:

    """An offer made on a particular item."""

    def __init__(self, item, offer=None, difficulty=None):
        self.item = item
        self.offer = offer
        self.difficulty = difficulty

        if not isinstance(item, Item):
            raise OfferError("Invalid Item provided to Offer: %s" % item)
    
    def __bool__(self):
        return bool(self.offer) and self.offer > 0
    
    def __int__(self):
        return self.offer or 0

    def __str__(self):
        if self: 
            return "%s: offering $%d (%d%%)" % (self.item, self.offer, 100 * self.offer / self.item.value)
        else:
            return "%s: No Offer" % self.item

def NoOffer(item):
    """Convenience function to retrieve a None Offer."""
    return Offer(item, None)

def OfferByPercent(item, percent, modifier=None, difficulty=None):
    """Convenience function to convert a percent of value to an Offer."""
    if not modifier: modifier = 0
    offer = round((percent / 100) * item.value * (1 + (modifier / 100)))
    return Offer(item, offer, difficulty)
