from bazaar import BazaarError, player_menu

def wizard_location(args):
    """Guide the user through the selection of a sales location for their items."""

    CONSIGNMENT = "consignment"
    PRIVATE_MARKET = "private market"

    response = player_menu("""
Select a location to sell your item(s):

1. consignment - put items up for consignment, NOT consuming any character
                 days, as the store handles the work

2. private market - consume a character day to seek a buyer directly
    """,
    {'c' : CONSIGNMENT, '1' : CONSIGNMENT,
     'p': PRIVATE_MARKET, '2' : PRIVATE_MARKET})

    if (response == CONSIGNMENT):
        args.consignment = True
    elif (response == PRIVATE_MARKET):
        args.privatemarket = True
    else:
        raise BazaarError("Invalid sales location selected")

    print()

def __get_ints():
    """Get integer responses from the console, space separated."""
    while True:
        try:
            response = input()
            if response: return [int(i) for i in response.split(' ')]
            return None
        except ValueError:
            print("Not a Number - try again!")

def wizard_items(args):
    """Guide the user through the entry of one or more items to sell."""

    print("Enter the value of each item you wish to sell on a separate line. Enter 0 when you are done.")

    if not args.itemvalues: args.itemvalues = []
    response = __get_ints()
    while response and response != [0]:
        args.itemvalues.extend(response)
        response = __get_ints()

    print()
