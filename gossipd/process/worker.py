""" gossipd
"""
from __future__ import absolute_import
import socket
import random
import re
import time
from tomcrypt import rsa
from gossipd.util.config import CONF
from gossipd.util.rsa import encrypt
from gossipd.file.model import Model
from gossipd.process.network import Socket

class Worker(Socket):
    """ Gossip
    """

    _model = None
    _name = None
    _challenge_pattern = None
    _message_pattern = None

    def __init__(self):
        random.seed()

        self._name = CONF.name
        self._model = Model()
        self._challenge_pattern = re.compile("challenge .+$")
        self._message_pattern = re.compile("message [a-zA-Z0-9_]+,.+$")

    def _relay_all_messages(self):
        for peer in self._model.get_peers():
            for message in self._model.get_messages(peer[0]):
                self._relay_message(peer, message)
            self._model.last_seen(peer[0])

    def _relay_message(self, peer, message):
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.connect((peer[2], peer[3]))
        except socket.error:
            print("Couldn't connect to peer %s @ %s:%d" % (peer[0], peer[2], peer[3]))
            return

        self._send(
            encrypt(
                peer[1],
                "%s,%s" % (
                    message[0],
                    message[1]
                )
            )
        )

        self._sock.close()
        self._sock = None

    def start(self):
        """ start
        """

        while True:
            try:
                action = random.randint(1, 5)
                if action == 1:
                    print("Relaying messages to peers.")
                    self._relay_all_messages()
                elif action == 2:
                    print("Generating an RSA key.")
                    key = rsa.Key(CONF.RSA_KEY_SIZE)
                    name = '-available'
                    if random.randint(1, 100) <= CONF.BOGUS_KEY_PCT:
                        name = '-bogus'
                    self._model.save_key(name, key.as_string())
                elif action == 3:
                    #bogus challenges
                    pass
                else:
                    print("Sleeping for %d seconds." % CONF.CLIENT_INTERVAL)
                    time.sleep(CONF.CLIENT_INTERVAL)
            except KeyboardInterrupt:
                print("Quitting worker.")
                exit(1)
