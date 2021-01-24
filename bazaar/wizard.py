from bazaar import BazaarError

def wizard_location(args):
    """Guide the user through the selection of a sales location for their items."""

    CONSIGNMENT = "consignment"
    PRIVATE_MARKET = "private market"

    response = player_menu("""
    Select a location to sell your item(s):

    1. consign - put items up for consignment, NOT consuming any character
                 days, as the store handles the work

    2. private market - consume a character day to seek a buyer directly
    """,
    {'c' : CONSIGNMENT, '1' : CONSIGNMENT,
     'p': PRIVATE_MARKET, '2' : PRIVATE_MARKET})

    if (reponse == CONSIGNMENT):
        args.consignment = True
    elif (response == PRIVATE_MARKET):
        args.privatemarket = True
    else:
        raise BazaarError("Invalid sales location selected")

def wizard_items(args):
    """Guide the user through the entry of one or more items to sell."""

    print("Enter the value of each item you wish to sell. Enter 0 when you are done.")

    response = int(input())
    while response != 0:
        args.itemvalues.append(response)
        response = int(input())

    if not args.itemvalues:
        raise BazaarError("No item values specified")
