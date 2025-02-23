import sqlite3
class DBManager:
    def __init__(self):
        self.db_path  = 'demo.db'

    def query(self, query):
        cursor = self.db.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def insert(self, values):
        cursor = self.db.cursor()
        values = [None] + list(values)
        prepared_statement = "INSERT INTO summarized (id, summary, file_path) VALUES (?, ?, ?) ON CONFLICT(file_path) DO UPDATE SET summary=excluded.summary"
        insert = cursor.execute(prepared_statement, values)
        self.db.commit()
        return insert

    def global_init(self):
        query = "CREATE TABLE IF NOT EXISTS summarized (id INTEGER PRIMARY KEY, summary TEXT, file_path TEXT UNIQUE)"
        cursor = self.db.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def __enter__(self):
        self.db = sqlite3.connect(self.db_path)
        return self
    
    def __exit__(self, a, b, c):
        self.db.close()