""" gossipd
"""
import os

class Configuration(object):
    """ Configuration
    """

    SOCKET_BACKLOG = 10
    MAX_NAME_LEN = 50
    OTP_RANGE_START = 2**128
    OTP_RANGE_END = 2**129
    MSGS_MAX_DIGITS = 4
    CHALLENGE_HASH_LEN = 64
    CLIENT_INTERVAL = 5
    RSA_KEY_SIZE = 4096
    BOGUS_KEY_PCT = 30

    def __init__(self):
        try:
            self.db_path = os.environ['GOSSIPD_DB_PATH']
        except KeyError:
            self.db_path = "gossipd.db"

        try:
            self.listen_ip = os.environ['GOSSIPD_LISTEN_IP']
        except KeyError:
            self.listen_ip = "127.0.0.1"

        try:
            self.listen_port = int(os.environ['GOSSIPD_LISTEN_PORT'])
        except KeyError:
            self.listen_port = 5555

        try:
            self.name = os.environ['GOSSIPD_USERNAME']
        except KeyError:
            print("You must define GOSSIPD_USERNAME environment variable.")
            exit(1)

CONF = Configuration()
