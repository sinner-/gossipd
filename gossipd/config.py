""" gossipd
"""
import sys

class Configuration(object):
    """ Configuration
    """

    SOCKET_BACKLOG = 10
    MAX_NAME_LEN = 50
    OTP_RANGE_START = 2**128
    OTP_RANGE_END = 2**129
    MSGS_MAX_DIGITS = 4
    CHALLENGE_HASH_LEN = 64

    db_path = "gossipd.db"

    listen_ip = "0.0.0.0"
    listen_port = 5555

    if sys.argv[1]:
        name = sys.argv[1]
    else:
        print("Must invoke the program with a name.")
        exit()


CONF = Configuration()
