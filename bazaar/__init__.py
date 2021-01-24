import random

class BazaarError (Exception):
    pass

def roll_vs_IQ(numdice, IQ):
    """Attempt one sales roll of `numdice`d6 vs `IQ` and return a boolean pass/fail."""
    roll = sum([random.randint(1, 6) for i in range(numdice)])
    return roll <= IQ

def player_menu(prompt, options):
    """Display an interactive menu and solicit one of the given options.
    
    prompt - plain text prompt to display first
    options - map of short responses to full display values

    Return will be the full display value (from options.values())
    """
    if isinstance(prompt, list):
        prompt = ' '.join([str(i) for i in prompt])
    print(prompt)
    print("Choose:", ', '.join(set(options.values())))
    while True:
        response = input()
        if response in options.values(): return response
        if response in options: return options[response]
        print("\nI don't understand. Please enter the option exactly.\nChoose:",
            ', '.join(set(options.values())))


def iterate_offers(items, offers):
    """Interactively consider each offer and accept or decline.

    Modify items and offers to remove any accepted.
    Return total sales price, in silver.
    """

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
