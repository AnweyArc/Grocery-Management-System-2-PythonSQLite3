import tkinter as tk
from tkinter import messagebox
import sqlite3

class DatabaseManager:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        try:
            # Create tables for store inventory, sales, and users
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS inventory (
                                    id INTEGER PRIMARY KEY,
                                    name TEXT,
                                    quantity INTEGER,
                                    price REAL
                                )""")

            self.cursor.execute("""CREATE TABLE IF NOT EXISTS sales (
                                    id INTEGER PRIMARY KEY,
                                    item_id INTEGER,
                                    item_name TEXT,
                                    quantity_sold INTEGER,
                                    sale_date TEXT,
                                    FOREIGN KEY (item_id) REFERENCES inventory(id)
                                )""")  

            self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                                    id INTEGER PRIMARY KEY,
                                    username TEXT UNIQUE,
                                    password TEXT,
                                    role TEXT
                                )""")  
            # Check if the users table is empty
            self.cursor.execute("SELECT COUNT(*) FROM users")
            count = self.cursor.fetchone()[0]
            if count == 0:
                # If the table is empty, set the first user as admin
                self.cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                                    ("admin", "admin", "Admin"))
                self.conn.commit()  # Commit the changes
        except sqlite3.Error as e:
            print("Error creating tables:", e)

    # User Management methods
    def register_user(self, username, password):
        try:
            # Set the role for subsequent users as "User"
            self.cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                                (username, password, "User"))
            self.conn.commit()
            messagebox.showinfo("Success", "User registered successfully.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error registering user: {e}")

    def login_user(self, username, password):
        try:
            self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                                (username, password))
            user = self.cursor.fetchone()
            if user:
                return user  # Return the user information
            else:
                return None  # Return None if user not found
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error logging in: {e}")

    def __del__(self):
        self.conn.close()

class UserManagementSystem:
    def __init__(self, master):
        # Initialize the main window for user authentication
        self.master = master
        self.master.title("User Authentication")
        self.master.geometry("400x200")
        self.db_manager = DatabaseManager("grocery_database.db")  # Changed database filename

        # Configure Background
        self.bg_color = "#cabeaf"
        self.button_color = "#b5485d"
        self.text_color = "black"
        self.text_color_white = "white"
        self.master.configure(bg=self.bg_color)

        # Title text
        self.title_label = tk.Label(self.master, text="User Authentication", bg=self.bg_color, fg=self.text_color, font=("Arial", 20, "bold"))
        self.title_label.pack()

        # Username and Password Entry
        self.username_label = tk.Label(self.master, text="Username:", bg=self.bg_color, fg=self.text_color, font=("Arial", 12))
        self.username_label.place(x=50, y=60)
        self.username_entry = tk.Entry(self.master, bg=self.bg_color, fg=self.text_color, font=("Arial", 12))
        self.username_entry.place(x=150, y=60)

        self.password_label = tk.Label(self.master, text="Password:", bg=self.bg_color, fg=self.text_color, font=("Arial", 12))
        self.password_label.place(x=50, y=100)
        self.password_entry = tk.Entry(self.master, bg=self.bg_color, fg=self.text_color, font=("Arial", 12), show="*")
        self.password_entry.place(x=150, y=100)

        # Buttons
        self.login_button = tk.Button(self.master, text="Login", bg=self.button_color, fg=self.text_color_white, font=("Arial", 12, "bold"), command=self.login)
        self.login_button.place(x=100, y=140)

        self.register_button = tk.Button(self.master, text="Register", bg=self.button_color, fg=self.text_color_white, font=("Arial", 12, "bold"), command=self.register)
        self.register_button.place(x=200, y=140)

    def login(self):
        # Functionality for user login
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = self.db_manager.login_user(username, password)
        if user:
            if user[3] == "Admin":  # Check if the user role is Admin
                messagebox.showinfo("Success", "Login successful as admin.")
                open_main_file()  # Open the admin file
            else:
                messagebox.showinfo("Success", "Login successful as regular user.")
                open_sell_items_file()  # Open the user file
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def register(self):
        # Functionality for user registration
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.db_manager.register_user(username, password)

def main():
    # Main function to initialize the application
    root = tk.Tk()
    app = UserManagementSystem(root)
    root.mainloop()

if __name__ == "__main__":
    # Run the main function if the script is executed directly
    main()
