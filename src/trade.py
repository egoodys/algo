"""
File:               trade.py
Python version:     3.4
Description:        Containers for trades.
"""

####################
from collections.abc import Sequence
####################
from db import DB
####################


class TradeClosedReason():
    """
    An enum.
    """
    reduced = 1
    manual = 2 # manually closed
    migrated = 3
    sl = 4 # stop loss
    tp = 5 # take profit
    ts = 6 # trailing stop
    margin_closeout = 7


class Trade():
    """
    Represents one trade, either past or present.
    Future trades are "opportunities" or "orders".
    """
    
    def __init__(self,
        broker_name=None,       # broker ID (name string) from databse
        instrument=None,        # TODO strings OK? Generic better.
        go_long=None,           # boolean
        stop_loss=None,         # numeric
        strategy=None,          # <Strategy>
        take_profit=None,       # numeric
        trade_id=None           # string
    ):
        self.broker_name    = broker_name
        self.instrument     = instrument
        self.go_long        = go_long
        self.stop_loss      = stop_loss
        self.strategy       = strategy
        self.take_profit    = take_profit
        self.trade_id       = trade_id
   

    def fill_in_extra_info(self):
        """
        Fill in info not provided by the broker, e.g.
        the name of the strategy that opened the trade.
 
        It's possible that a trade will be opened then the system is
        unexpectedly terminated before info about the trade can be saved to
        the database. Thus a trade passed to this
        function may not have a corresponding trade in the database.

        Returns: (nothing)
        """
        trade_info = DB.execute('SELECT strategy, broker, instrument_id FROM open_trades_live WHERE trade_id = {}'
            .format(self.trade_id))
        if len(trade_info) > 0:
            # verify broker and instrument match, just to be safe
            if trade_info[0][1] != self.broker_name:
                Log.write('"trade.py" fill_in_extra_info(): ERROR: "{}" != "{}"'
                    .format(trade_info[0][1], self.broker_name))
                raise Exception
            instrument = DB.execute('SELECT symbol FROM instruments WHERE id = {}'
                .format(trade_info[0][2]))
            if instrument[0][0] != self.instrument:
                Log.write('"trade.py" fill_in_extra_info(): {} != {}'
                    .format(instrument[0]['symbol'], self.instrument))
                raise Exception
            # save strategy
            self.strategy = None
            # TODO: good practice to access daemon's strategy list like this?
            for s in Daemon.strategies:
                if s.get_name == trade_info[0][0]:
                    self.strategy = s # reference to class instance
            # It might be possible that the trade was opened by a
            # strategy that is not running. In that case, use the default
            # strategy.
            self.strategy = Daemon.backup_strategy
            


    def __str__(self):

        strategy_name = "(unknown)"
        if self.strategy != None:
            strategy_name = self.strategy.name
        msg = 'Transaction ID: {}\n\
            Instrument: {}\n\
            Strategy: {}'\
            .format(
                self.trade_id,
                self.instrument,
                strategy_name
            )
        return msg


class Trades(Sequence):
    """
    List of `trade` objects.
    TODO:  This could be a heap, with the trade's ID as the key.
    """
    
    def __init__(self):
        self._trade_list = []
        self.current_index = 0

    def append(self, trade):
        self._trade_list.append(trade)


    def pop(self, trade_id):
        """
        Remove the trade with the given transaction ID.
        
        Returns: Removed trade object on success; None on failure.
        """
        index = 0
        for t in self._trade_list:
            if t.trade_id == trade_id:
                return self._trade_list.pop(index)
            index = index + 1
        return None


    def length(self):
        return len(self._trade_list)    


    def __str__(self):
        msg = ''
        for s in self._trade_list:
            msg = msg + str(s) + '\n'
        return msg


    def __iter__(self):
        """
        Make this class iterable
        https://docs.python.org/3/library/stdtypes.html#typeiter
        """
        return self


    def __next__(self):
        """
        Make this class iterable
        """
        if self.current_index >= len(self._trade_list):
            self.current_index = 0
            raise StopIteration
        else:
            self.current_index = self.current_index + 1
            return self._trade_list[self.current_index - 1]


    def __getitem__(self, key):
        """
        Expose index operator.
        """
        return self._trade_list[key]
    

    def __len__(self):
        """
        Expose len() function.
        """
        return len(self._trade_list)

