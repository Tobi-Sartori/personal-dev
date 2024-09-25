import sqlite3
import os


class CacheDB:
    _instance = None

    def __new__(cls, db_path="cache.db"):
        if cls._instance is None:
            cls._instance = super(CacheDB, cls).__new__(cls)
            db_exists = os.path.exists(db_path)

            if not db_exists:
                cls._instance.create_table()

            cls._instance.conn = sqlite3.connect(db_path)

        return cls._instance

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS cache (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        hash TEXT UNIQUE CHECK(length(hash) = 64),
                        response TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);
                    """)
        
        self.conn.commit()

    def get_response(self, hash):
        cursor = self.conn.cursor()
        cursor.execute("SELECT response FROM cache WHERE hash=?", (hash,))
        response = cursor.fetchone()

        return response[0] if response else None
    
    def store_response(self, question, hash, response):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO cache (question, hash, response) VALUES (?, ?, ?)", (question, hash, response))
        self.conn.commit()
    


