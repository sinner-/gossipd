""" gossipc
"""
from __future__ import absolute_import
import argparse
import os
from tomcrypt import rsa
from gossipd.db.model import Model
from gossipd.util.config import CONF

def main():
    """ main
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-a",
                        "--add-peer",
                        action="store_true",
                        dest="add_peer")
    parser.add_argument("-P",
                        "--set-peer-key",
                        action="store_true",
                        dest="set_peer_key")
    parser.add_argument("-d",
                        "--delete-peer",
                        action="store_true",
                        dest="delete_peer")
    parser.add_argument("-s",
                        "--send-message",
                        action="store_true",
                        dest="send_message")
    parser.add_argument("-g",
                        "--view-messages",
                        action="store_true",
                        dest="view_messages")
    parser.add_argument("-n",
                        "--name",
                        type=str,
                        dest="name")
    parser.add_argument("-H",
                        "--host",
                        type=str,
                        dest="host")
    parser.add_argument("-p",
                        "--port",
                        type=int,
                        dest="port")
    parser.add_argument("-k",
                        "--pubkey-file",
                        type=str,
                        dest="pubkey_file")
    parser.add_argument("-S",
                        "--source",
                        type=str,
                        dest="source")
    parser.add_argument("-m",
                        "--message",
                        type=str,
                        dest="message")
    args = parser.parse_args()

    if args.add_peer:
        if not args.name or not args.host or not args.port:
            print("You must call --add-peer with name, host and port.")
            exit(1)

        model = Model()
        keytext = model.assign_peer(args.name)
        if keytext:
            exchange_key = rsa.Key(keytext).public.as_string()
            model.save_peer(args.name, args.host, args.port)
            print("Exchange key:")
            print(exchange_key)
        else:
            print("No RSA keys available for assignment.")
            exit(1)
        exit(0)

    if args.set_peer_key:
        if not args.name or not args.pubkey_file:
            print("You must call --set-peer-key with name, pubkey-file.")
            exit(1)
        if not os.path.exists(args.pubkey_file):
            print("pubkey-file %s doesn't exist." % args.pubkey_file)
            exit(1)
        with open(args.pubkey_file) as key_file:
            model = Model()
            model.set_peer_key(args.name, key_file.read())
        exit(0)

    if args.delete_peer:
        if not args.name:
            print("You must call --delete-peer with name.")
            exit(1)
        model = Model()
        model.delete_peer(args.name)
        exit(0)

    if args.send_message:
        if not args.source or not args.message:
            print("You must call --send-message with source and message.")
            exit(1)
        model = Model()
        model.save_message('self', args.source, args.message)
        exit(0)

    if args.view_messages:
        model = Model()
        for message in model.view_messages():
            print(message)
        exit(0)
