import sqlite3

class DatabaseManager:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Create tables for store inventory and store database
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS inventory (
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                quantity INTEGER,
                                price REAL
                            )""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS sales (
                                id INTEGER PRIMARY KEY,
                                item_id INTEGER,
                                quantity_sold INTEGER,
                                sale_date TEXT,
                                FOREIGN KEY (item_id) REFERENCES inventory(id)
                            )""")

        # Create table for user information
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                username TEXT UNIQUE,
                                password TEXT
                            )""")
        self.conn.commit()

    # Store Inventory methods
    def add_item(self, name, quantity, price):
        try:
            self.cursor.execute("INSERT INTO inventory (name, quantity, price) VALUES (?, ?, ?)",
                                (name, quantity, price))
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error adding item to inventory:", e)

    def view_inventory(self):
        try:
            self.cursor.execute("SELECT name, quantity, price FROM inventory")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print("Error viewing inventory:", e)
            return []

    def clear_inventory(self):
        try:
            self.cursor.execute("DELETE FROM inventory")
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error clearing inventory:", e)

    # Store Database methods
    def view_sales(self):
        try:
            self.cursor.execute("SELECT * FROM sales")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print("Error viewing sales:", e)
            return []

    def clear_sales(self):
        try:
            self.cursor.execute("DELETE FROM sales")
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error clearing sales:", e)

    # User methods
    def register_user(self, username, password):
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                                (username, password))
            self.conn.commit()
            print("User registered successfully.")
        except sqlite3.Error as e:
            print("Error registering user:", e)

    def login_user(self, username, password):
        try:
            self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                                (username, password))
            user = self.cursor.fetchone()
            if user:
                print("Login successful.")
                return True
            else:
                print("Invalid username or password.")
                return False
        except sqlite3.Error as e:
            print("Error logging in:", e)

    def __del__(self):
        self.conn.close()
