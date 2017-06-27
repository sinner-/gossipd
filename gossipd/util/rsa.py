""" gossipd
"""
import base64
from tomcrypt import rsa

def encrypt(keytext, message):
    """ encrypt
    """

    pubkey = rsa.Key(keytext)
    if len(message) < pubkey.max_payload():
        return base64.b64encode(
            pubkey.encrypt(
                message.encode('ascii')
            )
        ).decode()
    else:
        return None

def decrypt(keytext, message):
    """ decrypt
    """

    key = rsa.Key(keytext)

    try:
        return key.decrypt(
            base64.b64decode(
                message
            )
        ).decode()
    except:
        return None
