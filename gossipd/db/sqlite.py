""" gossipd
"""
from __future__ import absolute_import
import sqlite3
from gossipd.util.config import CONF

class DB(object):
    """ DB
    """

    _conn = None

    def __init__(self):
        self._conn = sqlite3.connect(CONF.db_path)
        cursor = self._conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS keys (
                peer VARCHAR(%d),
                key TEXT
            );''' % CONF.MAX_NAME_LEN)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS peers (
                name VARCHAR(%d),
                public_key TEXT,
                host VARCHAR(255),
                port INT,
                last_seen DATETIME
            );''' % CONF.MAX_NAME_LEN)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                timestamp DATETIME,
                sender VARCHAR(%d),
                delivered_by VARCHAR(%d),
                message TEXT
            );''' % (CONF.MAX_NAME_LEN, CONF.MAX_NAME_LEN))
        self.commit()
        cursor.close()

    def get_cursor(self):
        """ get_cursor
        """

        return self._conn.cursor()

    def commit(self):
        """ commit
        """
        self._conn.commit()
