""" gossipd
"""
from gossipd.util.config import CONF

class Socket(object):
    """ Socket
    """

    _sock = None

    def _send(self, message):
        if self._sock:
            self._sock.sendall(
                ("%0*d%s" % (
                    CONF.MSGS_MAX_DIGITS,
                    len(message),
                    message
                )).encode('ascii')
            )

    def _recv(self):
        if self._sock:
            data = ''.encode('ascii')
            payload_size = int(self._sock.recv(CONF.MSGS_MAX_DIGITS))
            while len(data) < payload_size:
                packet = self._sock.recv(payload_size - len(data))
                if not packet:
                    return None
                data += packet
            print(data.decode())
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
