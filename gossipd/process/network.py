""" gossipd
"""
from __future__ import absolute_import
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

    def _recv(self):
        if self._sock:
            data = ''.encode('ascii')
            try:
                payload_size = int(self._sock.recv(CONF.MSGS_MAX_DIGITS))
            except ValueError:
                self._error("error_expecting_response")
            while len(data) < payload_size:
                packet = self._sock.recv(payload_size - len(data))
                if not packet:
                    return None
                data += packet
            print("RECV: %s" % data.decode())
            return data.decode()
        return None

    def _close(self):
        if self._sock:
            self._sock.shutdown(1)
            self._sock.close()
            self._sock = None

    def _error(self, message):
        self._send(message)
        self._close()
