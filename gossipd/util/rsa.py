""" gossipd
"""
import base64
from tomcrypt import rsa

def encrypt(keytext, challenge):
    """ encrypt
    """

    pubkey = rsa.Key(keytext)

    return base64.b64encode(
        pubkey.encrypt(
            challenge.encode('ascii')
        )
    ).decode()

def decrypt(keytext, challenge):
    """ decrypt
    """

    key = rsa.Key(keytext)

    try:
        return key.decrypt(
            base64.b64decode(
                challenge
            )
        ).decode()
    except:
        return None
