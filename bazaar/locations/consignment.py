import random

from bazaar import roll_vs_IQ, player_menu, iterate_offers
from bazaar.offer import Offer, NoOffer, OfferByPercent

def get_percent(dice):
    """Add a d20 to the base percent for the difficulty.
    Return the offered percent of item value."""
    basepercent = 10 + dice * 10
    return basepercent + random.randint(1, 20)


def find_best_offer_at(dice, IQ, item, modifier):

    """Return the best available offer at a given die roll.

    Additional attempts continue until either the character misses the
    roll against IQ, or the offer found is lower than the last.
    
    Return an Offer object with the best offer at this difficulty.
    """
    bestpercent = 0
    while roll_vs_IQ(dice, IQ):
        percent = get_percent(dice)
        if (percent >= bestpercent):
            bestpercent = percent
        else: break
    if bestpercent:
        return OfferByPercent(item, percent, modifier, dice)
    return NoOffer(item)


def consign_item(IQ, item, modifier):

    """Determine the best available price for one item on one day.
    
    IQ - character's adjusted IQ to roll against
    item - the Item to be sold
    modifier - modifier to apply, if any (e.g. 25 for +25%)
    
    Return an Offer object with the best offer for the day.
    """

    bestoffer = NoOffer(item)
    dice = 3
    while True:
        offer = find_best_offer_at(dice, IQ, item, modifier)
        if not offer: break
        if int(offer) > int(bestoffer):
            bestoffer = offer
        dice += 1
    return bestoffer


def consign_items(IQ, items, modifier):
    """Determine the best available price for each item on one day."""
    return [consign_item(IQ, item, modifier) for item in items]


def consign_sell(IQ, items, modifier):

    """Offer interactive consignment over the course of one town week.
    
    Modify `items` to remove any items sold.
    Return total sales price, in silver.
    """

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    sales_total = 0
    open_offers = [NoOffer(item) for item in items]
    for day in days:
        if not items:
            break

        # Summarize progress
        print()
        print('-' * (len(day) + 2))
        print(day, ":")
        print('-' * (len(day) + 2))
        print()
        print("Attempting to sell", len(items), "items by consignment.")
        if (sales_total): print("Earned so far: $%d" % sales_total)

        # Try to keep yesterday's offers alive
        open_offers = [
            offer if (offer and roll_vs_IQ(offer.difficulty, IQ)) else NoOffer(offer.item)
            for offer in open_offers]

        # Print and save today's best offers
        print("\nOffers available today:")
        for i in reversed(range(len(items))):
            offer = consign_item(IQ, items[i], modifier)
            if (offer and int(offer) >= int(open_offers[i])):
                open_offers[i] = offer
                print(open_offers[i])
            elif (open_offers[i]):
                print(open_offers[i], "* (existing offer)")
            else:
                print(open_offers[i]) # NoOffer

        # Process bulk offer response
        response = player_menu("", {
            'a': "accept all",
            'd': "decline all",
            's': "some of each",
            'q': "quit the marketplace"})
        
        if response == "accept all":
            for i in reversed(range(len(open_offers))):
                if open_offers[i]:
                    items.pop(i)
                    sales_total += int(open_offers[i])
        elif response == "decline all":
            pass
        elif response == "quit the marketplace":
            break
        elif response == "some of each":
            sales_total += iterate_offers(items, open_offers)
        else:
            raise BazaarError("Invalid offer response selected")

    return sales_total
