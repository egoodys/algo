#!/usr/bin/python3

# Python ver.    3.4
# File:         strategy.py
# Description:  Base class for strategies

#*************************
#*************************
from trade import trade
#*************************

class strategy():

    def __init__(self):
        self.name = None
        """
        Strategies track their trades for a few reasons:
        - The strategy might need to babysit the position.
        - Use open trades to make decisions regarding new trades.
        """
        self.open_trades = []  # list of trades opened by this strategy. 


    def callback_trade_opened(self, trade):
        """
        This is used to notify the strategy when an order that it suggested
        was placed.

        This is separate from callback_recover_trade() because originally
        this function was going to save the trade to the database. However,
        that has been moved to the daemon, immediately after an order is
        placed. But I'm nonetheless keeping this function separate for now.
        """
        self.open_trades.append(trade)


    def callback_trade_closed(self, transaction_id):
        """
        This is used to notify the strategy that one of its trades has closed.
        Returns: Bool (True if trade was aware of trade before being notified)
        """
        # Remove the trade from the list. 
        closed_trade = None
        for i in range(1, len(self.open_trades)):
            if self.open_trades[i].transaction_id == transaction_id:
                closed_trade = self.open_trades.pop[i-1]
        if closed_trade == None:
            return False
        else:
            return True


    def callback_recover_trade(self, trade):
        """
        When the daemon is initializing, particularly after being unexpectedly
        terminated, this can be used to tell the strategy
        module about a trade that it had previously opened.
        """
        self.open_trades.append(trade)


    def refresh(self):
        """
        Look at current price and past prices and determine whether there is
        an opportunity or not.
        Returns:
            If the daemon should enter a trade, an instance of `order',
            otherwise None.
        """
        self.babysit()
        return self.scan()


    def babysit(self):
        raise NotImplementedError()


    def scan(self):
        raise NotImplementedError()

