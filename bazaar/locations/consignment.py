from bazaar import roll_vs_IQ, get_percent, player_menu
from bazaar.offer import Offer, NoOffer, OfferByPercent

def find_best_offer_at(dice, IQ, item, modifier):

    """Return the best available offer at a given die roll.

    Additional attempts continue until either the character misses the
    roll against IQ, or the offer found is lower than the last.
    
    Return an Offer object with the best offer at this difficulty.
    """
    bestpercent = 0
    while roll_vs_IQ(dice, IQ):
        percent = get_percent(dice * 10 + 10)
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


def iterate_offers(items, offers):
    """Interactively consider each offer and accept or decline."""
    sales_total = 0
    for i in reversed(range(len(items))):
        if not offers[i]: continue
        print()
        response = player_menu(
            offers[i],
            {'a' : "accept", 'y' : "accept",
             'd' : "decline", 'n' : "decline"})
        if (response == "accept"):
            items.pop(i)
            sales_total += int(offers.pop(i))
    return sales_total

def consign_sell(IQ, items, modifier):

    """Offer interactive consignment over the course of one town week.
    
    Modify `items` to remove any items sold.
    Return total sales price, in silver.
    """

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    sales_total = 0
    for day in days:
        if not items:
            break

        # Summarize progress
        print()
        print('-' * (len(day) + 2))
        print(day, ":")
        print('-' * (len(day) + 2))
        print()
        print("Attempting to sell", len(items), "items")
        if (sales_total): print("Earned so far: $%d" % sales_total)

        # Print today's offers
        print("\nOffers available today:")
        offers = consign_items(IQ, items, modifier)
        for offer in reversed(offers):
            print(offer)

        # Process bulk offer response
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

    return sales_total
