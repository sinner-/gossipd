""" gossipd
"""
import base64
from tomcrypt import rsa

def encrypt(keytext, message):
    """ encrypt
    """

    try:
        pubkey = rsa.Key(keytext)
    except:
        print("Public key format error.")
        return None

    if len(message) < pubkey.max_payload():
        return base64.b64encode(
            pubkey.encrypt(
                message.encode('ascii')
            )
        )

    return None

def decrypt(keytext, message):
    """ decrypt
    """

    try:
        key = rsa.Key(keytext)
    except:
        print("Private key format error.")
        return None

    try:
        return key.decrypt(
            base64.b64decode(
                message
            )
        ).decode()
    except:
        return None
