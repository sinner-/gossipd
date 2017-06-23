""" gossipd
"""
from gossipd.daemon import Daemon

def main():
    """ launcher
    """
    gossipd = Daemon()
    gossipd.start()
