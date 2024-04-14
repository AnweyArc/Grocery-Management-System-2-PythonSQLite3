import sqlite3

class DatabaseManager:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS groceries (
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                quantity INTEGER,
                                price REAL
                            )""")
        self.conn.commit()


    def __del__(self):
        self.conn.close()
