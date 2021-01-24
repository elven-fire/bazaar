from bazaar import roll_vs_IQ, get_offer, format_offer, player_menu

def find_best_offer_at(dice, IQ):

    """Return the best available offer at a given die roll.

    Additional attempts continue until either the character misses the
    roll against IQ, or the offer found is lower than the last.
    
    Return a percent integer [1-100], or None for no offer.
    """
    bestoffer = 0
    while roll_vs_IQ(dice, IQ):
        offer = get_offer(dice * 10 + 10)
        if (offer >= bestoffer):
            bestoffer = offer
        else: break
    return bestoffer or None

def find_best_offer(IQ):

    """Return the best available multiplier today.
    
    IQ - character's adjusted IQ to roll against
    
    Return a percent integer [1-100], or None for no offer.
    """

    bestoffer = 0
    dice = 3
    while True:
        offer = find_best_offer_at(dice, IQ)
        if offer is None: break
        if offer > bestoffer:
            bestoffer = offer
        dice += 1
    return bestoffer or None


def consign_item(IQ, value, modifier):

    """Determine the best available price for one item on one day.
    
    IQ - character's adjusted IQ to roll against
    value - the normal value of the item to sell, in silver
    modifier - modifier to apply, if any (e.g. 25 for +25%)
    
    Return the best offer, in silver, or None for no offer.
    """

    offer = find_best_offer(IQ)
    if offer is None: return None
    if modifier is None: modifier = 0
    return offer * (value / 100) * (1 + (modifier / 100))


def consign_items(IQ, itemvalues, modifier):
    """Determine the best available price for each item on one day."""
    return [consign_item(IQ, value, modifier) for value in itemvalues]

def iterate_offers(itemvalues, offers):
    """Interactively consider each offer and accept or decline."""
    sales_total = 0
    for i in reversed(range(len(itemvalues))):
        if offers[i] is None: continue
        print()
        response = player_menu(
            format_offer(itemvalues[i], offers[i]),
            {'a' : "accept", 'y' : "accept",
             'd' : "decline", 'n' : "decline"})
        if (response == "accept"):
            itemvalues.pop(i)
            sales_total += offers.pop(i)
    return sales_total

def consign_sell(IQ, itemvalues, modifier):

    """Offer interactive consignment over the course of one town week.
    
    Modify itemvalues to remove any items sold.
    Return total sales price, in silver.
    """

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    sales_total = 0
    for day in days:
        if not itemvalues:
            break

        # Summarize progress
        print()
        print('-' * (len(day) + 2))
        print(day, ":")
        print('-' * (len(day) + 2))
        print()
        print("Attempting to sell", len(itemvalues), "items")
        if (sales_total): print("Earned so far: $", sales_total)

        # Print today's offers
        print("\nOffers available today:")
        offers = consign_items(IQ, itemvalues, modifier)
        for value, offer in zip(reversed(itemvalues), reversed(offers)):
            print(format_offer(value, offer))

        # Process bulk offer response
        response = player_menu("", {
            'a': "accept all",
            'd': "decline all",
            's': "some of each",
            'q': "quit the marketplace"})
        
        if response == "accept all":
            for i in reversed(range(len(itemvalues))):
                if offers[i] is not None:
                    itemvalues.pop(i)
                    sales_total += offers[i]
        elif response == "decline all":
            pass
        elif response == "quit the marketplace":
            break
        elif response == "some of each":
            sales_total += iterate_offers(itemvalues, offers)
        else:
            raise BazaarError("Invalid offer response selected")

    return sales_total
