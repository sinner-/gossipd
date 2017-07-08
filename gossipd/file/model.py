""" gossipd
"""
from __future__ import absolute_import
import os
import shutil
import random
import hashlib
import datetime
from gossipd.util.config import CONF

class Model(object):
    """ Model
    """

    def __init__(self):
        self._keys_path = "%s/keys" % CONF.gossipd_dir
        self._peers_path = "%s/peers" % CONF.gossipd_dir
        self._messages_path = "%s/messages" % CONF.gossipd_dir

        try:
            os.makedirs(CONF.gossipd_dir)
            os.makedirs(self._keys_path)
            os.makedirs(self._peers_path)
            os.makedirs(self._messages_path)
        except:
            pass

    def get_peers(self):
        """ get_peers
        """

        peers = []

        for peer_name in os.listdir(self._peers_path):
            if not os.path.exists("%s/%s/public_key" % (self._peers_path, peer_name)):
                continue

            peer = []
            peer.append(peer_name)
            with open('%s/%s/public_key' % (self._peers_path, peer_name), 'r') as public_key:
                peer.append(public_key.read())
            with open('%s/%s/peer_info' % (self._peers_path, peer_name), 'r') as peer_info:
                peer_components = peer_info.read().split(":")
                peer.append(peer_components[0])
                peer.append(int(peer_components[1]))

            peers.append(peer)

        return peers

    def save_peer(self, name, host, port):
        """ save_peer
        """

        try:
            os.makedirs('%s/%s' % (self._peers_path, name))
        except:
            pass
        with open('%s/%s/peer_info' % (self._peers_path, name), 'w') as peer_info:
            peer_info.write("%s:%s" % (host, port))

    def delete_peer(self, name):
        """ delete_peer
        """

        #TODO: move key for user from assigned to bogus
        #os.rename('%s/%s' % (self._assigned_path, name), '%s/%s' % (self._bogus_path, name))
        shutil.rmtree('%s/%s' % (self._peers_path, name))

    def last_seen(self, name):
        """ last_seen
        """

        os.utime('%s/%s/peer_info' % (self._peers_path, name), None)

    def set_peer_key(self, name, key_text):
        """ set_peer_key
        """

        with open('%s/%s/public_key' % (self._peers_path, name), 'w') as public_key:
            public_key.write("%s" % key_text)

    def get_messages(self, name):
        """ get_messages
        """

        messages = []

        if not os.path.exists("%s/%s/public_key" % (self._peers_path, name)):
            return messages

        last_seen = datetime.datetime.fromtimestamp(os.path.getmtime("%s/%s/peer_info" % (self._peers_path, name)))

        for message_path in os.listdir(self._messages_path):
            message_timestamp = datetime.datetime.fromtimestamp(os.path.getmtime("%s/%s" % (self._messages_path, message_path)))
            if message_timestamp > last_seen:
                message = []
                with open("%s/%s" % (self._messages_path, message_path), 'r') as message_data:
                    message_components = message_data.read().split(",", 3)
                    if message_components[0] == "*local" or message_components[1] == name:
                        continue
                    message.append(message_components[0])
                    message.append(message_components[2])
                messages.append(message)

        return messages

    def view_messages(self):
        """ view_messages
        """

        messages = []

        for message_path in os.listdir(self._messages_path):
            message = []
            message.append(str(datetime.datetime.fromtimestamp(os.path.getmtime("%s/%s" % (self._messages_path, message_path)))))
            with open("%s/%s" % (self._messages_path, message_path), 'r') as message_data:
                message_components = message_data.read().split(",", 3)
                for component in message_components:
                    message.append(component)
            messages.append(message)

        return messages

    def save_message(self, sender, delivered_by, message):
        """ save_messages
        """

        message_hash = hashlib.sha256(("%d%s%s%s" % (random.getrandbits(8), sender, delivered_by, message)).encode()).hexdigest()
        with open('%s/%s' % (self._messages_path, message_hash), 'w') as message_data:
            message_data.write("%s,%s,%s" % (sender, delivered_by, message))

    def save_key(self, key_type, key_text):
        """ save_key
        """

        key_hash = hashlib.sha256(key_text.encode()).hexdigest()

        with open('%s/%s' % (self._keys_path, key_hash), 'w') as key_data:
            key_data.write("%s\n%s" % (key_type, key_text))

    def get_keys(self):
        """ get_keys
        """

        keys = []

        for key_path in os.listdir(self._keys_path):
            key = []
            with open("%s/%s" % (self._keys_path, key_path), 'r') as key_data:
                key.append(key_data.readline().strip())
                key.append(key_data.read())
            keys.append(key)

        return keys

    def assign_peer(self, name):
        """ assign_peer
        """

        available_key = None

        for key_path in os.listdir(self._keys_path):
            with open("%s/%s" % (self._keys_path, key_path), 'r') as key_data:
                key_name = key_data.readline().strip()
                key_text = key_data.read()
                if not available_key and key_name == "-available":
                    available_key = (key_path, key_text)
            if key_name == name:
                with open("%s/%s" % (self._keys_path, key_path), 'w') as key_data:
                    key_data.write("%s\n%s" % ('-bogus', key_text))

        if available_key:
            with open("%s/%s" % (self._keys_path, available_key[0]), 'w') as key_data:
                key_data.write("%s\n%s" % (name, available_key[1]))
            return available_key[1]

        return None
