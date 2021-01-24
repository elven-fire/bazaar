import random

from bazaar import roll_vs_IQ, player_menu, iterate_offers
from bazaar.offer import OfferByPercent, NoOffer

def sell_item(IQ, item, modifier):

    """Determine the best available price for one item on one day.

    IQ - character's adjusted IQ to roll against
    item - the Item to be sold
    modifier - modifier to apply, if any (e.g. 25 for +25%)

    Return an Offer object with the best offer for the day.
    """

    dice = 4
    if roll_vs_IQ(dice, IQ):
        percent = 50 + random.randint(1, 20)

        while roll_vs_IQ(dice + 1, IQ):
            percent += random.randint(1, 20)
            dice += 1

        return OfferByPercent(item, percent, modifier, dice)
    else: return NoOffer(item)

def sell_items(IQ, items, modifier):
    """Determine the best available price for each item on one day."""
    return [sell_item(IQ, item, modifier) for item in items]


def market_sell(IQ, items, modifier):

    """Offer interactive private market sales for up to one town week.

    Modify `items` to remove any items sold.
    Return total sales price, in silver.
    """

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    sales_total = 0
    for day in days:

        # Summarize progress
        print()
        print('-' * (len(day) + 2))
        print(day, ":")
        print('-' * (len(day) + 2))
        print()
        print("Attempting to sell", len(items), "items on the private market.")
        if (sales_total): print("Earned so far: $%d" % sales_total)

        # Print today's best offers
        offers = sell_items(IQ, items, modifier)
        print("\nOffers available today:")
        for offer in reversed(offers):
            print(offer)

        # Process bulk offer response
        if (any(offers)):
            response = player_menu("", {
                'a': "accept all",
                'd': "decline all",
                's': "some of each",
                'q': "quit the marketplace"})

            if response == "accept all":
                for i in reversed(range(len(offers))):
                    if offers[i]:
                        items.pop(i)
                        sales_total += int(offers[i])
            elif response == "decline all":
                pass
            elif response == "quit the marketplace":
                break
            elif response == "some of each":
                sales_total += iterate_offers(items, offers)
            else:
                raise BazaarError("Invalid offer response selected")

        # Prompt to consume another day
        if items and day != 'Friday':
            print()
            print("You still have %d items remaining to sell." % len(items))
            response = player_menu(
                "Would you like to try again tomorrow, using another day?",
                {'y': "yes", 'n': "no"})
            if response == "no":
                break

    return sales_total
