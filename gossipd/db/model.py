""" gossipd
"""
from __future__ import absolute_import
from gossipd.db.sqlite import DB

class Model(object):
    """ Model
    """

    _db = None

    def __init__(self):
        self._db = DB()

    def check_peer(self, name):
        """ check_peer
        """

        cursor = self._db.get_cursor()
        result = cursor.execute("""
            SELECT COUNT(name)
            FROM peers
            WHERE name = ?
            LIMIT 1
        """, (name,)).fetchone()[0]
        cursor.close()
        if result > 0:
            return True
        return False

    def get_peers(self):
        """ get_peers
        """

        cursor = self._db.get_cursor()
        peers = cursor.execute("""
            SELECT name, public_key, host, port
            FROM peers
            WHERE public_key IS NOT NULL
        """).fetchall()
        cursor.close()
        return peers

    def get_peer_key(self, name):
        """ get_peer_key
        """

        cursor = self._db.get_cursor()
        peer_key = cursor.execute("""
            SELECT public_key
            FROM peers
            WHERE name = ?
            LIMIT 1
        """, (name,)).fetchone()[0]
        cursor.close()
        return peer_key

    def save_peer(self, name, host, port):
        """ save_peer
        """

        cursor = self._db.get_cursor()
        cursor.execute("""
            INSERT INTO peers
            VALUES (
                ?, NULL, ?, ?, datetime('now')
            )
        """, (name, host, port))
        cursor.close()

    def delete_peer(self, name):
        """ delete_peer
        """

        cursor = self._db.get_cursor()
        cursor.execute("""
            UPDATE keys
            SET name = '_bogus'
            WHERE name = ?
        """, (name,))
        cursor.execute("""
            DELETE FROM peers
            WHERE name = ?
        """, (name,))
        self._db.commit()
        cursor.close()

    def last_seen(self, name):
        """ last_seen
        """

        cursor = self._db.get_cursor()
        cursor.execute("""
            UPDATE peers
            SET last_seen = datetime('now')
            WHERE name = ?
        """, (name,))
        self._db.commit()
        cursor.close()

    def set_peer_key(self, name, keyfile):
        """ set_peer_key
        """

        cursor = self._db.get_cursor()
        cursor.execute("""
            UPDATE peers
            SET public_key = ?
            WHERE name = ?
        """, (keyfile, name))
        self._db.commit()
        cursor.close()

    def get_messages(self, name):
        """ get_messages
        """

        cursor = self._db.get_cursor()
        messages = cursor.execute("""
            SELECT sender, message
            FROM messages
            WHERE delivered_by != ?
            AND timestamp > (
                SELECT last_seen
                FROM peers
                WHERE name = ?
                LIMIT 1
            )
        """, (name, name,)).fetchall()
        cursor.close()
        return messages

    def view_messages(self):
        """ view_messages
        """

        cursor = self._db.get_cursor()
        messages = cursor.execute("""
            SELECT timestamp, delivered_by, sender, message
            FROM messages
        """).fetchall()
        cursor.close()
        return messages

    def save_message(self, sender, delivered_by, message):
        """ save_messages
        """

        cursor = self._db.get_cursor()
        cursor.execute("""
            INSERT INTO messages
            VALUES (datetime('now'), ?, ?, ?)
        """, (sender, delivered_by, message))
        self._db.commit()
        cursor.close()

    def save_key(self, name, key):
        """ save_key
        """

        cursor = self._db.get_cursor()
        cursor.execute("""
            INSERT INTO keys
            VALUES (?, ?)
        """, (name, key))
        self._db.commit()
        cursor.close()

    def get_key(self, name):
        """ get_key
        """

        cursor = self._db.get_cursor()
        key = cursor.execute("""
            SELECT key
            FROM keys
            WHERE peer = ?
            LIMIT 1
        """, (name,)).fetchone()[0]
        cursor.close()
        return key

    def assign_peer(self, name):
        """ assign_peer
        """

        cursor = self._db.get_cursor()

        #we only want one key per peer
        cursor.execute("""
            UPDATE keys
            SET peer = '_bogus'
            WHERE peer = ?
        """, (name,))
        if cursor.rowcount() > 0:
            self._db.commit()

        cursor.execute("""
            UPDATE keys
            SET peer = ?
            WHERE key = (
                SELECT key
                FROM keys
                WHERE peer = '_available'
                LIMIT 1
            )
        """, (name,))

        exchange_key = None
        if cursor.rowcount() > 0:
            self._db.commit()
            exchange_key = cursor.execute("""
                SELECT key
                FROM keys
                WHERE peer = ?
            """, (name,)).fetchone()[0]
        cursor.close()
        return exchange_key

