"""
Run the daemon here.
"""

####################
import cmd
import curses
from threading import Thread
####################
from daemon import Daemon
####################


if __name__ == "__main__":
    curses.wrapper(Daemon.run)

