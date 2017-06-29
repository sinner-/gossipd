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
            print("SEND: %s" % message)
            self._sock.sendall(message)
            self._sock.send("\n".encode('ascii'))

    def _recv(self):
        if not self._sock:
            return None

        data = ''.encode('ascii')
        while True:
            packet = self._sock.recv(CONF.RECV_BYTES)
            if not packet:
                break
            data += packet
            if packet[-1] == CONF.NEW_LINE_CHAR:
                break

        print("RECV: %s" % data.decode())
        return data.decode()

    def _close(self):
        if self._sock:
            self._sock.shutdown(1)
            self._sock.close()
            self._sock = None

    def _error(self, message):
        self._send(message)
        self._close()
