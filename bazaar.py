import argparse

from bazaar import BazaarError
from bazaar.offer import Item
from bazaar.wizard import wizard_location, wizard_items
from bazaar.locations.consignment import consign_sell
from bazaar.locations.privatemarket import market_sell

VERSION = '0.1.0'

def parse_args():
    parser = argparse.ArgumentParser(description="Assist in selling items in Elven Fire towns.")

    # Require the character's IQ
    parser.add_argument('-i', "--IQ", type=int, required=True, help="adjusted IQ of the character selling items")

    # Accept up to one argument indicating where to sell
    loc_group = parser.add_mutually_exclusive_group(required=False)
    loc_group.add_argument('-c', "--consignment", action='store_true', help="sell items by consignment, without consuming a character day")
    loc_group.add_argument('-p', "--private-market", action='store_true', dest='privatemarket', help="sell items on the private market, consuming character days")

    # Accept the values of items to be sold
    parser.add_argument('-v', "--value", type=int, nargs='*', dest='itemvalues', help="specify the value of item(s) to be sold, in silver")

    # Accept a modifier to be applied to the final sales price
    parser.add_argument('-m', "--modifier", type=int, help="final modifier to apply to the sale price (e.g. -m 25 to add 25 percent to the final offer)")

    return parser.parse_args()


def main(args):
    print(args)

    # Prompt the user for sales location and/or items as needed
    if not (args.consignment or args.privatemarket):
        wizard_location(args)
    if not args.itemvalues:
        wizard_items(args)

    # Continue to sell the items
    sales_total = 0
    items = [Item(value) for value in args.itemvalues]
    if args.consignment:
        sales_total += consign_sell(args.IQ, items, args.modifier)
    elif args.privatemarket:
        sales_total += market_sell(args.IQ, items, args.modifier)
    else:
        raise BazaarError("No sales location determined")
    
    print("\nThanks for visiting the bazaar!")
    if (sales_total): print("You earned: $%d" % sales_total)
    if (items):
        print("You have", len(items), "items left unsold:")
        for item in items:
            print(" - %s" % item)


if __name__ == '__main__':
    main(parse_args())
