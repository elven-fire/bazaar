import random

from bazaar import roll_vs_IQ, player_menu
from bazaar.locations import _InteractiveSalesLocation
from bazaar.offer import OfferByPercent, NoOffer

class PrivateMarket(_InteractiveSalesLocation):

    def get_offer_for_item(self, item):

        """Determine the best available Offer for one item on one day."""

        dice = 4
        if roll_vs_IQ(dice, self.IQ):
            percent = 50 + random.randint(1, 20)

            while roll_vs_IQ(dice + 1, self.IQ):
                percent += random.randint(1, 20)
                dice += 1

            return OfferByPercent(item, percent, self.modifier, dice)
        else: return NoOffer(item)

    def end_of_day(self, day):
        """Prompt the player before consuming another day."""
        if self.items and day != self.DAYS[-1]:
            print()
            print("You still have %d items remaining to sell." % len(self.items))
            response = player_menu(
                "Would you like to try again tomorrow, using another day?",
                {'y': "yes", 'n': "no"})
            return response == "yes"
        return True
