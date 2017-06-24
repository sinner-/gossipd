""" gossipd
"""

class Configuration(object):
    """ Configuration
    """

    SOCKET_BACKLOG = 10
    MAX_NAME_LEN = 50
    OTP_RANGE_START = 2**128
    OTP_RANGE_END = 2**129
    MSGS_MAX_DIGITS = 4

    db_path = "gossipd.db"

    listen_ip = "0.0.0.0"
    listen_port = 5555

CONF = Configuration()
