""" gossipd
"""
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
        return cursor.execute("""
            SELECT name, key, my_key, host, port
            FROM peers
        """).fetchall()

    def get_messages(self, name):
        """ get_messages
        """

        cursor = self._db.get_cursor()
        messages = cursor.execute("""
            SELECT sender, message
            FROM messages
            WHERE timestamp > (
                SELECT last_seen
                FROM peers
                WHERE name = ?
                LIMIT 1
            )
        """, (name,)).fetchall()
        cursor.close()
        return messages

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

    def save_message(self, peer, name, message):
        """ save_messages
        """

        cursor = self._db.get_cursor()
        cursor.execute("""
            INSERT INTO messages
            VALUES (datetime('now'), ?, ?, ?)
        """, (name, peer, message))
        self._db.commit()
        cursor.close()
