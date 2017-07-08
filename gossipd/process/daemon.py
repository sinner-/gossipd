""" gossipd
"""
from __future__ import absolute_import
import socket
import re
from gossipd.process.network import Socket
from gossipd.util.rsa import decrypt
from gossipd.util.config import CONF
from gossipd.file.model import Model

class Daemon(Socket):
    """ Gossip
    """

    _model = None
    _ascii_pattern = None
    _message_pattern = None
    _server = None

    def __init__(self):
        self._model = Model()

        self._ascii_pattern = re.compile("[\x00-\x7F]+$")
        self._payload_pattern = re.compile("[a-zA-Z0-9_]+,[\x00-\x7F]+$")

        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self._server.bind((CONF.listen_ip, CONF.listen_port))
        except:
            print("Couldn't bind to socket. Daemon exiting. Worker is probably still running.")
            exit(1)
        self._server.listen(CONF.SOCKET_BACKLOG)

    def start(self):
        """ start
        """

        while True:
            try:
                self._sock, _ = self._server.accept()

                data = self._recv()

                if data and self._ascii_pattern.match(data):
                    for privkey in self._model.get_keys():
                        payload = decrypt(privkey[1], data)
                        if payload and self._payload_pattern.match(payload):
                            payload = payload.split(",", 1)
                            self._model.save_message(
                                payload[0],
                                privkey[0],
                                payload[1]
                            )

            except KeyboardInterrupt:
                print("Quitting daemon.")
                exit(1)
