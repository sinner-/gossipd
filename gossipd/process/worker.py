""" gossipd
"""
from __future__ import absolute_import
import socket
import random
import re
import time
from tomcrypt import rsa
from gossipd.util.rsa import decrypt
from gossipd.util.config import CONF
from gossipd.db.model import Model
from gossipd.process.network import Socket

class Worker(Socket):
    """ Gossip
    """

    _model = None
    _name = None
    _challenge_pattern = None
    _messages_pattern = None
    _message_pattern = None

    def __init__(self):
        random.seed()

        self._name = CONF.name
        self._model = Model()
        self._challenge_pattern = re.compile("challenge .+$")
        self._messages_pattern = re.compile("messages [0-9]{%d}" % CONF.MSGS_MAX_DIGITS)
        self._message_pattern = re.compile("message [a-zA-Z0-9_]+,.+$")

    def _get_all_messages(self):
        peers = self._model.get_peers()
        for peer in peers:
            self._get_messages(peer)

    def _get_messages(self, peer):
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.connect((peer[2], peer[3]))
        except socket.error:
            print("Couldn't connect to peer %s @ %s:%d" % (peer[0], peer[2], peer[3]))
            return

        self._send("hello %s" % self._name)
        data = self._recv()
        if data and self._challenge_pattern.match(data):
            peer_key = self._model.get_key(peer[0])
            challenge = decrypt(peer_key, data.split(" ", 1)[1])
            if challenge:
                self._send("response %s" % challenge)
                data = self._recv()
                if data and self._messages_pattern.match(data):
                    incoming = int(data.split(" ")[1])

                    for _ in range(incoming):
                        data = self._recv()
                        if data and self._message_pattern.match(data):
                            message = data.split(",", 1)
                            self._model.save_message(message[0].split(" ")[1],
                                                     peer[0],
                                                     message[1])
                        else:
                            self._error("bad_message")
                            break
                else:
                    self._error("bad_challenge")
            else:
                self._error("bad_messages")
        else:
            self._error("bad_challenge")

        self._sock.close()
        self._sock = None

    def start(self):
        """ start
        """

        while True:
            try:
                action = random.randint(1, 5)
                if action == 1:
                    print("Fetching messages from peers.")
                    self._get_all_messages()
                elif action == 2:
                    print("Generating an RSA key.")
                    key = rsa.Key(CONF.RSA_KEY_SIZE)
                    name = '_available'
                    if random.randint(1, 100) <= CONF.BOGUS_KEY_PCT:
                        name = '_bogus'
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
