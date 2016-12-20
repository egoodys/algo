#!/usr/bin/python 

"""
File:           opportunities.py
Python verion:  3.4

The `opportunity` class is a potential order plus meta information about the order.

The `opportunities` class is a list of opportunities.
"""
import log

class opportunity():
    """
    """

    def __init__(self):

        # type: int 1-100
        # description: estimated rating of success
        self.confidence = 1
        # type: string
        # description: ID (name) of strategy
        self.strategy = None
        # type: <order object>
        # description: Order object that can be passed to broker API
        self.order = None

    def __str__(self):
        return 'opportunity'

    
class opportunities():
    
    #
    def __init__(self):
        self.opportunities = []

    def __str__(self):
        return 'opportunities'

    def push(self, opp):
        """
        Take an opportunity dict and add it to the list.
        """
        self.opportunities.append(opp)

    def pop (self, instrument):
        """
        Find and return the best opportunity.
        If there are no opportunities, return an empty dict.
        If an error occurs, return None.
        """
        # Just pick the one with the highest confidence rating.
        max_conf_index = -1
        max_conf = 0
        if self.opportunities == []:
            return {}
        for i in xrange(0, len(self._opportunities) - 1):
            if self._opportunities[i]['confidence'] > max_conf:
                max_conf_index = i
        return self.opportunities.pop(max_conf_index)
        


