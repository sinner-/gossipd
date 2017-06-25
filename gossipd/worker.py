""" gossipd
"""
import socket
import random
import re
import time
from gossipd.util.gpg import decrypt
from gossipd.db.model import Model
from gossipd.config import CONF

class Worker(object):
    """ Gossip
    """

    _model = None
    _sock = None
    _name = None
    _challenge_pattern = None
    _messages_pattern = None
    _message_pattern = None

    def __init__(self):
        random.seed()

        self._name = CONF.name
        self._model = Model()
        self._challenge_pattern = re.compile("(challenge [a-z0-9]{64})$")
        self._messages_pattern = re.compile("messages [0-9]{%d}" % CONF.MSGS_MAX_DIGITS)
        self._message_pattern = re.compile("message [a-zA-Z0-9_]+,.+$")

    def _send(self, message):
        if self._sock:
            self._sock.sendall(
                bytes(
                    "%0*d%s" % (
                        CONF.MSGS_MAX_DIGITS,
                        len(message),
                        message
                    ),
                    'ascii'
                )
            )

    def _recv(self):
        if self._sock:
            data = bytes('', 'ascii')
            payload_size = int(self._sock.recv(CONF.MSGS_MAX_DIGITS))
            while len(data) < payload_size:
                packet = self._sock.recv(payload_size - len(data))
                if not packet:
                    return None
                data += packet
            return data.decode()
        return None

    def _get_all_messages(self):
        peers = self._model.get_peers()
        for peer in peers:
            self._get_messages(peer)

    def _get_messages(self, peer):
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.connect((peer[3], peer[4]))
        except ConnectionRefusedError:
            print("Couldn't connect to peer %s @ %s:%d" % (peer[0], peer[3], peer[4]))
            return

        self._send("hello %s" % self._name)
        data = self._recv()
        if self._challenge_pattern.match(data):
            challenge = decrypt(self._name, data.split(" ")[1])
            self._send("response %s" % challenge)

            data = self._recv()
            if data and self._messages_pattern.match(data):
                incoming = int(data.split(" ")[1])

                for _ in range(incoming):
                    data = self._recv()
                    if self._message_pattern.match(data):
                        message = data.split(",", 1)
                        self._model.save_message(self._name, message[0], message[1])

                self._model.last_seen(peer[0])

        self._sock.close()
        self._sock = None

    def start(self):
        """ start
        """

        while True:
            action = random.randint(1, 10)
            if action == 1:
                self._get_all_messages()
            elif action == 2:
                #generate RSA keys
                pass
            elif action == 3:
                #bogus challenges
                pass
            else:
                time.sleep(CONF.CLIENT_INTERVAL)
