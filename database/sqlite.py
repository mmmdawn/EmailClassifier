import sqlite3
from utils.logger_utils import get_logger

logger = get_logger('SQLite')


class SQLiteDatabse:
    def __init__(self, name: str = 'knowledge.db'):
        self._conn = sqlite3.connect(name)

    def close(self):
        self._conn.close()

    def create_tables(self):
        cursor = self._conn.cursor()

        cursor.execute('''
            DROP TABLE IF EXISTS prior_probs;
        ''')

        cursor.execute('''
            DROP TABLE IF EXISTS cond_probs;
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prior_probs (
                label INTEGER PRIMARY KEY,
                prob REAL
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cond_probs (
                word TEXT PRIMARY KEY,
                ham REAL,
                spam REAL
            );
        ''')

        try:
            self._conn.commit()
        except Exception as e:
            logger.exception(e)

    def insert_knowledge(self, prior_probs, cond_probs):
        cursor = self._conn.cursor()

        for label, prob in prior_probs.items():
            cursor.execute('''
                INSERT INTO prior_probs (label, prob)
                VALUES (?, ?)
            ''', (label, prob))

        for word, labels_probs in cond_probs.items():
            ham_prob = labels_probs[0]
            spam_prob = labels_probs[1]
            cursor.execute('''
                INSERT INTO cond_probs (word, ham, spam)
                VALUES (?, ?, ?)
            ''', (word, ham_prob, spam_prob))

        try:
            self._conn.commit()
        except Exception as e:
            logger.exception(e)

    def get_prior_probs(self):
        cursor = self._conn.cursor()
        cursor.execute('''
            SELECT * FROM prior_probs
        ''')

        prior_probs = {}
        for label, prob in cursor.fetchall():
            prior_probs[label] = prob
        return prior_probs

    def get_cond_probs(self, words):
        cursor = self._conn.cursor()
        cond_probs = {}
        for word in words:
            cursor.execute('''
                SELECT * FROM cond_probs
                WHERE word=?
            ''', (word,))
            row = cursor.fetchone()
            if row:
                ham_prob = row[1]
                spam_prob = row[2]
                cond_probs[word] = (ham_prob, spam_prob)
        return cond_probs


if __name__ == '__main__':
    db = SQLiteDatabse()
    db.create_tables()
