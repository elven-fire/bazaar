from bazaar import player_menu

class _SalesLocation:

    """Location where a player can sell items during the week.

    IQ - character's adjusted IQ to roll against
    items - list of the Items to be sold
    modifier - modifier to apply, if any (e.g. 25 for +25%)
    sales_total - total silver earned through sales
    """

    DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    def __init__(self, IQ, items, modifier=None):
        self.IQ = IQ
        self.modifier = modifier
        self.items = items
        self.sales_total = 0

    def get_offer_for_item(self, item):
        """Determine the best available Offer for one item on one day."""
        raise NotImplementedError

    def get_daily_offers(self):
        """Determine the best available Offer for each item on one day."""
        return [self.get_offer_for_item(item) for item in self.items]


class _InteractiveSalesLocation(_SalesLocation):

    def print_daily_summary(self, day):
        """Print a daily header and current status to the console."""
        print()
        print('-' * (len(day) + 2))
        print(day, ":")
        print('-' * (len(day) + 2))
        print()
        print("Attempting to sell", len(self.items), "items.")
        if (self.sales_total):
            print("Earned so far: $%d" % self.sales_total)

    def print_daily_offers(self, offers):
        """Print all offers to the console for review."""
        print("\nOffers available today:")
        for offer in offers:
            print(offer)

    def start_day(self, day):
        """Do start-of-day processing and return whether to continue selling."""
        return True

    def end_of_day(self, day):
        """Do end-of-day processing and return whether to continue selling."""
        return True

    def _accept_offer(self, index, offer):
        """Accept the offer, selling the item at the given index."""
        self.items.pop(index)
        self.sales_total += int(offer)

    def _iterate_offers(self, offers):
        """Interactively consider each offer and accept or decline."""
        for i in reversed(range(len(self.items))):
            if not offers[i]: continue
            print()
            response = player_menu(
                offers[i],
                {'a' : "accept", 'y' : "accept",
                'd' : "decline", 'n' : "decline"})
            if (response == "accept"):
                self._accept_offer(i, offers.pop(i))

    def _process_offers(self, offers):

        """Interactively accept or decline offers in bulk.

        Return whether to continue selling.
        """

        if not any(offers):
            return True

        response = player_menu("", {
            'a': "accept all",
            'd': "decline all",
            's': "some of each",
            'q': "quit the marketplace"})

        if response == "accept all":
            for i in reversed(range(len(offers))):
                if offers[i]:
                    self._accept_offer(i, offers[i])
        elif response == "decline all":
            pass
        elif response == "quit the marketplace":
            return False
        elif response == "some of each":
            self._iterate_offers(offers)
        else:
            raise BazaarError("Invalid offer response selected")

        return bool(self.items)

    def interactive_sell(self):

        """Offer interactive sales over the course of one town week.

        Modify `items` to remove any items sold.
        Return total sales price, in silver.
        """

        for day in self.DAYS:
            if not self.items:
                break

            # Provide a hook for start-of-day processing
            keep_selling = self.start_day(day)
            if not keep_selling: break

            # Summarize progress
            self.print_daily_summary(day)

            # Get and print today's offers
            offers = self.get_daily_offers()
            self.print_daily_offers(offers)

            # Interactively process offer responses
            keep_selling = self._process_offers(offers)
            if not keep_selling: break

            # Provide a hook for end-of-day processing
            keep_selling = self.end_of_day(day)
            if not keep_selling: break

        return self.sales_total
