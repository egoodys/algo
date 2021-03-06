# -*- coding: utf-8 -*-

"""
File            broker_api.py
Python ver.     3.4
Description:
    Python module that provides a generic layer between
    the daemon and the broker-specific code.
"""

#****************************
import configparser
import sys
#****************************
from config import Config
from log import Log
from oanda import Oanda
#****************************

class Broker():

    # Using a broker variable eliminates conditionals in the methods.
    broker = None
    if Config.broker_name == 'oanda':
        broker = Oanda
    else:
        DB.bug('"broker.py": unknown broker "{}"'.format(Config.broker_name))
        raise Exception


    # Get authorization key.
    @classmethod
    def get_auth_key(cls):
        """ 
        Oanda uses an authentication key for HTTP requests.
        """
        return cls.broker.get_auth_key()


    # Get list of accounts
    # Returns: dict or None
    @classmethod
    def get_accounts(cls):
        return cls.broker.get_accounts()
   
 
    # Get list of open positions
    # Returns: dict or None 
    @classmethod
    def get_positions(cls, account_id):
        return cls.broker.get_positions(account_id)


    # Get number of positions for a given account ID
    # Returns: Integer
    @classmethod
    def get_num_of_positions(cls, account_id):
        return cls.broker.get_num_of_positions(account_id)


    # Get account balance for a given account ID
    # Returns: Decimal number
    @classmethod
    def get_balance(cls, account_id):
        return cls.broker.get_balance(account_id)


    @classmethod
    def get_prices(cls, instruments, since=None):
        """
        Fetch live prices for specified symbol(s)/instrument(s).
        Returns: dict or None
        TODO: make this more robust. Maybe pass in a list, then have each broker-specific library
            do validation.
        """
        return cls.broker.get_prices(instruments, since)


    @classmethod
    def get_ask(cls, instrument, since=None):
        """
        Get one ask price
        Returns: Decimal or None
        """
        return cls.broker.get_ask(instrument, since)


    @classmethod
    def get_bid(cls, instrument, since=None):
        """
        # Get one bid price
        # Returns: Decimal or None
        """
        return cls.broker.get_bid(instrument, since)


    @classmethod
    def get_spreads(cls, instruments, since=None):
        """
        """
        return cls.broker.get_spreads(instruments, since)


    @classmethod
    def get_spread(cls, instrument, since=None):
        return cls.broker.get_spread(instrument, since)


    @classmethod
    def place_order(cls, order):
        """
        Place an order.
        
        Return: TODO: develop generic format for all brokers
        """
        result = cls.broker.place_order(order)
        # TODO: If a trade is opened, write trade info to db
        # (table: open_trades_live)
        return result

    @classmethod
    def is_market_open(cls):
        """
        Is the market open?

        Returns: Boolean
        """
        return cls.broker.is_market_open()


    @classmethod
    def get_transaction_history(cls, maxId=None, minId=None, count=None, instrument=None, ids=None):
        """
        # Get transaction history
        # Returns: dict or None
        """
        return cls.broker.get_transaction_history(maxId=maxId, minId=minId,
            count=count, instrument=instrument, ids=ids)


    @classmethod
    def is_trade_closed(cls, transaction_id):
        """
        See if a trade is closed.
        Returns: 
        """
        return cls.broker.is_trade_closed(transaction_id)


    @classmethod
    def get_trades(cls):
        """
        Get info about all open trades from the broker.
        To get "local" info about the trades, use
        trade.fill_in_trade_extra_info().

        Returns: instance of <trades>
        """
        return cls.broker.get_trades()


    """
    Get info about a particular trade
    Returns: instance of <trade>
    """
    @classmethod
    def get_trade(cls, trade_id):
        return cls.broker.get_trade(trade_id)


    # Get order info
    # Returns: dict or None
    @classmethod
    def get_order_info(cls, order_id):
        return cls.broker.get_order_info(order_id)

 
    @classmethod
    def modify_order(cls, order_id, units=0, price=0, expiry=0,
        lower_bound=0, upper_bound=0, stop_loss=0,
        take_profit=0, trailing_stop=0):
        """
        # Modify an existing order
        # Returns: dict or None
        """
        return cls.broker.modify_orders(locals())


    @classmethod
    def modify_trade(cls, trade_id, stop_loss=0, take_profit=0, trailing_stop=0):
        """
        # Modify an existing trade
        # Returns: dict or None
        """
        return cls.broker.modify_trade(
            trade_id = trade_id,
            stop_loss = stop_loss,
            take_profit = take_profit,
            trailing_stop = trailing_stop
        )


