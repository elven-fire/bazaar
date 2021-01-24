import random

from bazaar import roll_vs_IQ, player_menu
from bazaar.offer import Offer, NoOffer, OfferByPercent
from bazaar.locations import _InteractiveSalesLocation

class Consignment(_InteractiveSalesLocation):

    def __init__(self, IQ, items, modifier=None):
        _InteractiveSalesLocation.__init__(self, IQ, items, modifier)
        self.open_offers = [NoOffer(item) for item in items]

    def _accept_offer(self, index, offer):
        """Accept the offer, selling the item at the given index."""
        self.open_offers.pop(index)
        _InteractiveSalesLocation._accept_offer(self, index, offer)

    def start_day(self, day):
        """Try to keep yesterday's offers alive."""
        if day != self.DAYS[0]:
            self.open_offers = [
                offer if (offer and roll_vs_IQ(offer.difficulty, self.IQ))
                    else NoOffer(offer.item)
                for offer in self.open_offers]
        return True

    def print_daily_offers(self, offers):
        """Print today's offers, noting existing offers held open."""
        print("\nOffers available today:")
        for i in reversed(range(len(offers))):
            if (offers[i] and int(offers[i]) >= int(self.open_offers[i])):
                self.open_offers[i] = offers[i]
                print(self.open_offers[i])
            elif (self.open_offers[i]):
                print(self.open_offers[i], "* (existing offer)")
            else:
                print(self.open_offers[i]) # NoOffer

    def get_offer_for_item(self, item):
        """Determine the best available Offer for one item on one day."""
        bestoffer = NoOffer(item)
        dice = 3
        while True:
            offer = self._find_best_offer_at(dice, item)
            if not offer: break
            if int(offer) > int(bestoffer):
                bestoffer = offer
            dice += 1
        return bestoffer

    def _get_percent(self, dice):
        """Add a d20 to the base percent for the difficulty.
        Return the offered percent of item value."""
        basepercent = 10 + dice * 10
        return basepercent + random.randint(1, 20)

    def _find_best_offer_at(self, dice, item):

        """Return the best available offer at a given die roll.

        Additional attempts continue until either the character misses the
        roll against IQ, or the offer found is lower than the last.
        
        Return an Offer object with the best offer at this difficulty.
        """
        bestpercent = 0
        while roll_vs_IQ(dice, self.IQ):
            percent = self._get_percent(dice)
            if (percent >= bestpercent):
                bestpercent = percent
            else: break
        if bestpercent:
            return OfferByPercent(item, percent, self.modifier, dice)
        return NoOffer(item)
