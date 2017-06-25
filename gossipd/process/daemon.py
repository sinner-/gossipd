""" gossipd
"""
import socket
import random
import hashlib
import re
from gossipd.process.network import Socket
from gossipd.util.gpg import encrypt
from gossipd.util.config import CONF
from gossipd.db.model import Model

class Daemon(Socket):
    """ Gossip
    """

    _model = None
    _hello_pattern = None
    _server = None

    def __init__(self):
        random.seed()

        self._model = Model()

        self._hello_pattern = re.compile("(hello [a-zA-Z0-9_]+)$")

        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind((CONF.listen_ip, CONF.listen_port))
        self._server.listen(CONF.SOCKET_BACKLOG)

    def start(self):
        """ start
        """

        while True:
            self._sock, _ = self._server.accept()

            data = self._recv()

            if data and self._hello_pattern.match(data):
                name = data.split(" ")[1]

                if not self._model.check_peer(name):
                    self._error("unknown_peer")
                    continue

                challenge = hashlib.sha256(
                    str(
                        random.randint(CONF.OTP_RANGE_START, CONF.OTP_RANGE_END)
                    ).encode('ascii')
                ).hexdigest()

                self._send("challenge %s" % encrypt(name, challenge))

                response = self._recv()

                if response == "response %s" % challenge:
                    messages = self._model.get_messages(name)
                    self._send("messages %0*d" % (CONF.MSGS_MAX_DIGITS, len(messages)))
                    for message in messages:
                        self._send(
                            "message %s,%s" % (
                                message[0],
                                message[1]
                            )
                        )

                    self._model.last_seen(name)
                    self._close()
                else:
                    self._error("bad_otp")
            else:
                self._error("bad_hello")
