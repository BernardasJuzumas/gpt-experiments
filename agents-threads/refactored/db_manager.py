import sqlite3
from pathlib import Path
from config import DATABASE_FOLDER, SEED

class DBManager:
    def __init__(self, seed):
        self.seed = seed
        self.conn = self.initialize_db()

    @staticmethod
    def cache_seed_directory(seed):
        Path(f"{DATABASE_FOLDER}/{seed}").mkdir(parents=True, exist_ok=True)

    def initialize_db(self):
        self.cache_seed_directory(self.seed)
        db_path = f"{DATABASE_FOLDER}/{self.seed}/log.db"
        conn = sqlite3.connect(db_path)
        conn.execute("""CREATE TABLE IF NOT EXISTS log (
                        timestamp text,
                        thread_id text,
                        run_id text,
                        assistant_id text
                    )""")
        return conn

    def execute(self, query, params=None):
        with self.conn as connection:
            cursor = connection.cursor()
            result = cursor.execute(query, params or ())
            return result.fetchall()

    def close(self):
        self.conn.close()
    def get_last_thread_and_run_id(self):
        query = """
            SELECT thread_id, run_id 
            FROM log 
            ORDER BY timestamp DESC 
            LIMIT 1;
        """
        result = self.execute(query)
        return result[0] if result else (None, None)


# Add more database-related functions if needed


