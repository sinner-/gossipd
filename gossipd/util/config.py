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
    RSA_KEY_SIZE = 1024
    BOGUS_KEY_PCT = 30

    try:
        db_path = os.environ['GOSSIPD_DB_PATH']
    except KeyError:
        db_path = "gossipd.db"

    try:
        listen_ip = os.environ['GOSSIPD_LISTEN_IP']
    except KeyError:
        listen_ip = "127.0.0.1"

    try:
        listen_port = int(os.environ['GOSSIPD_LISTEN_PORT'])
    except KeyError:
        listen_port = 5555

    try:
        name = os.environ['GOSSIPD_USERNAME']
    except KeyError:
        print("You must define GOSSIPD_USERNAME environment variable.")
        exit(1)

CONF = Configuration()
