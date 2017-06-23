""" gossipd
"""
import sqlite3
from gossipd.config import CONF

class DB(object):
    """ DB
    """

    _conn = None

    def __init__(self):
        self._conn = sqlite3.connect(CONF.db_path)
        cursor = self._conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS keys (
                name VARCHAR(%d),
                public_key TEXT,
                private_key TEXT
            );''' % CONF.MAX_NAME_LEN)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS peers (
                name VARCHAR(%d),
                key TEXT,
                my_key TEXT,
                host VARCHAR(255),
                port INT,
                last_seen DATETIME
            );''' % CONF.MAX_NAME_LEN)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                timestamp DATETIME,
                from VARCHAR(%d),
                source VARCHAR(%d),
                message TEXT
            );''' % (CONF.MAX_NAME_LEN, CONF.MAX_NAME_LEN))
        cursor.commit()
        cursor.close()
