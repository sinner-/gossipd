""" gossipd
"""
from __future__ import absolute_import
from gossipd.util.rsa import encrypt
from gossipd.util.rsa import decrypt
from gossipd.util.config import CONF

class Socket(object):
    """ Socket
    """

    _sock = None

    def _send(self, message):
        if self._sock:
            payload = (
                ("%0*d%s" % (
                    CONF.MSGS_MAX_DIGITS,
                    len(message),
                    message
                )).encode('ascii')
            )
            print("SEND: %s" % payload.decode())
            self._sock.sendall(payload)

    def _ssend(self, peer_keytext, message):
        self._send(
            encrypt(peer_keytext, message)
        )

    def _recv(self):
        if self._sock:
            data = ''.encode('ascii')
            header = self._sock.recv(CONF.MSGS_MAX_DIGITS)
            if header:
                payload_size = int(header)
                while len(data) < payload_size:
                    packet = self._sock.recv(payload_size - len(data))
                    if not packet:
                        return None
                    data += packet
                print("RECV: %s" % data.decode())
                return data.decode()
            else:
                self._error("bad_header")
        return None

    def _srecv(self, priv_keytext):
        payload = self._recv()
        if payload:
            return decrypt(priv_keytext, payload)
        else:
            return None

    def _close(self):
        if self._sock:
            self._sock.shutdown(1)
            self._sock.close()
            self._sock = None

    def _error(self, message):
        self._send(message)
        self._close()
