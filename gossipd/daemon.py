""" gossipd
"""
import socket
import random
import hashlib
import re
from util.gpg import encrypt
from db.sqlite import DB
from config import CONF

class Daemon(object):
    """ Gossip
    """

    _db = None
    _hello_pattern = None
    _sock = None
    _conn = None

    def __init__(self):
        random.seed()

        self._db = DB()

        self._hello_pattern = re.compile("(hello [a-zA-Z0-9]+)$")

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((CONF.listen_ip, CONF.listen_port))
        self._sock.listen(CONF.SOCKET_BACKLOG)

    def _send(self, message):
        if self._conn:
            self._conn.send(bytes("%s\n" % message, 'ascii'))

    def _recv(self, payload_size):
        if self._conn:
            data = self._conn.recv(payload_size)
            if data:
                return data.decode().strip()
        return None

    def _close(self):
        if self._conn:
            self._conn.shutdown(1)
            self._conn.close()
            self._conn = None

    def _error(self, message):
        self._send(message)
        self._close()

    def start(self):
        """ start
        """

        while True:
            self._conn, _ = self._sock.accept()

            data = self._recv(len("hello ") + CONF.MAX_NAME_LEN + 1)

            if data and self._hello_pattern.match(data):
                hello = data.split(" ")

                name = hello[1].strip()

                if name not in peers.keys():
                    self._error("unknown_peer")
                    continue

                challenge = hashlib.sha256(
                    str(
                        random.randint(CONF.OTP_RANGE_START, CONF.OTP_RANGE_END)
                    )
                ).hexdigest()

                self._send("challenge %s" % encrypt(name, challenge))

                response = self._recv(len("response ") + len(challenge) + 1)

                if response and response == "response %s" % challenge:
                    self._send("messages %d" % len(messages))
                    for message in messages:
                        #TODO: should probably transmit message length
                        self._send(
                            "message %s,%s,%s,%s" % (
                                message['time'],
                                message['from'],
                                message['source'],
                                message['text']
                            )
                        )

                    #TODO:
                    #recv #!messages N
                    #loop N times recv message and append

                    self._close()
                else:
                    self._error("bad_otp\n")
