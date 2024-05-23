import tkinter as tk
from tkinter import ttk, messagebox
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
                                name TEXT UNIQUE,
                                quantity INTEGER,
                                price REAL
                            )""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS sales (
                                id INTEGER PRIMARY KEY,
                                item_id INTEGER,
                                quantity_sold INTEGER,
                                FOREIGN KEY (item_id) REFERENCES inventory(id)
                            )""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                username TEXT UNIQUE,
                                password TEXT
                            )""")
        self.conn.commit()

    def search_item(self, item_name):
        try:
            self.cursor.execute("SELECT name, price, quantity FROM inventory WHERE name LIKE ?", ('%' + item_name + '%',))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print("Error searching item:", e)
            return []

    def add_item(self, name, quantity, price):
        try:
            self.cursor.execute("SELECT id, quantity FROM inventory WHERE name=?", (name,))
            result = self.cursor.fetchone()
            if result:
                current_id, current_quantity = result
                new_quantity = current_quantity + quantity
                self.cursor.execute("UPDATE inventory SET quantity=? WHERE id=?", (new_quantity, current_id))
            else:
                self.cursor.execute("INSERT INTO inventory (name, quantity, price) VALUES (?, ?, ?)",
                                    (name, quantity, price))
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error adding item to inventory:", e)

    def view_inventory(self):
        try:
            self.cursor.execute("SELECT name, price, quantity FROM inventory")
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

    def delete_item(self, item_name):
        try:
            self.cursor.execute("DELETE FROM inventory WHERE name=?", (item_name,))
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error deleting item:", e)

    def get_item_by_name(self, item_name):
        try:
            self.cursor.execute("SELECT * FROM inventory WHERE name=?", (item_name,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print("Error retrieving item:", e)

    def edit_item(self, item_id, new_name, new_quantity, new_price):
        try:
            self.cursor.execute("UPDATE inventory SET name=?, quantity=?, price=? WHERE id=?",
                                (new_name, new_quantity, new_price, item_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error editing item:", e)

    def __del__(self):
        self.conn.close()


class GroceryManagementSystem:
    def __init__(self, master):
        self.master = master
        self.master.title("Grocery Management System")
        self.db_manager = DatabaseManager("grocery_database.db")

        self.bg_color = "#cabeaf"
        self.button_color = "#b5485d"
        self.text_color = "black"
        self.text_color_white = "white"

        self.master.configure(bg=self.bg_color)

        self.title_label = tk.Label(self.master, text="Grocery Management System", bg=self.bg_color, fg=self.text_color, font=("Arial", 20, "bold"))
        self.title_label.place(x=575, y=20)
        self.title_label = tk.Label(self.master, text="Inventory Dashboard", bg=self.bg_color, fg=self.text_color, font=("Arial", 15, "bold"))
        self.title_label.place(x=670, y=60)

        self.store_inventory_button = tk.Button(self.master, text="Store Inventory", bg=self.button_color, fg=self.text_color_white, font=("Arial", 12, "bold"), command=self.open_inventory_window)
        self.store_inventory_button.place(x=700, y=100, width=150, height=30)

        self.show_items_button = tk.Button(self.master, text="Show Items", bg=self.button_color, fg=self.text_color_white, font=("Arial", 12, "bold"), command=self.show_items)
        self.show_items_button.place(x=700, y=150, width=150, height=30)

        self.item_prices_label = tk.Label(self.master, text="Item Prices", bg=self.bg_color, fg=self.text_color, font=("Arial", 12, "bold"))
        self.item_prices_label.place(x=730, y=190)

        # SearchEntry1
        self.item_prices_entry = tk.Entry(self.master, bg=self.bg_color, fg=self.text_color, font=("Arial", 10))
        self.item_prices_entry.place(x=704, y=220, width=140)
        self.item_prices_entry.bind("<KeyRelease>", self.search_items)

        # Treeview1
        self.item_prices_tree = ttk.Treeview(self.master, columns=("name", "price", "quantity"), show="headings")
        self.item_prices_tree.heading("name", text="Item Name")
        self.item_prices_tree.heading("price", text="Item Price")
        self.item_prices_tree.heading("quantity", text="Quantity Left")
        self.item_prices_tree.column("name", width=120)
        self.item_prices_tree.column("price", width=100)
        self.item_prices_tree.column("quantity", width=80)
        self.item_prices_tree.place(x=580, y=250, width=380, height=200)

        self.current_window = None

    def open_inventory_window(self):
        if self.current_window:
            self.current_window.destroy()

        inventory_window = tk.Toplevel(self.master)
        inventory_window.title("Store Inventory")
        inventory_window.geometry("900x600")
        inventory_window.configure(bg=self.bg_color)

        title_label = tk.Label(inventory_window, text="Store Inventory", bg=self.bg_color, fg="black", font=("Arial", 20, "bold"))
        title_label.place(x=477, y=20)

        add_items_button = tk.Button(inventory_window, text="Add Items", bg=self.button_color, fg=self.text_color_white, font=("Arial", 10, "bold"), command=self.add_items)
        add_items_button.place(x=50, y=100, width=130, height=40)

        delete_item_button = tk.Button(inventory_window, text="Delete an Item", bg=self.button_color, fg=self.text_color_white, font=("Arial", 10, "bold"), command=self.delete_item_window)
        delete_item_button.place(x=50, y=150, width=130, height=40)

        edit_items_button = tk.Button(inventory_window, text="Edit Items", bg=self.button_color, fg=self.text_color_white, font=("Arial", 10, "bold"), command=self.edit_items)
        edit_items_button.place(x=50, y=200, width=130, height=40)

        view_inventory_button = tk.Button(inventory_window, text="View Inventory", bg=self.button_color, fg=self.text_color_white, font=("Arial", 10, "bold"), command=self.view_inventory)
        view_inventory_button.place(x=50, y=250, width=130, height=40)

        clear_inventory_button = tk.Button(inventory_window, text="Clear Inventory", bg=self.button_color, fg=self.text_color_white, font=("Arial", 10, "bold"), command=self.confirm_clear_inventory)
        clear_inventory_button.place(x=50, y=300, width=130, height=40)

        # Create search entry and store it as an attribute
        self.search_entry = tk.Entry(inventory_window, bg=self.bg_color, fg=self.text_color, font=("Arial", 10))
        self.search_entry.place(x=50, y=350, width=130)
        self.search_entry.bind("<KeyRelease>", self.search_items)

        # Treeview2
        self.info_tree = ttk.Treeview(inventory_window, columns=("name", "price", "quantity"), show="headings")
        self.info_tree.heading("name", text="Item Name")
        self.info_tree.heading("price", text="Item Price")
        self.info_tree.heading("quantity", text="Quantity Left")
        self.info_tree.column("name", width=200)
        self.info_tree.column("price", width=150)
        self.info_tree.column("quantity", width=150)
        self.info_tree.place(x=280, y=100, width=600, height=400)

        self.current_window = inventory_window

    def search_items(self, event=None):
        search_query = self.item_prices_entry.get()
        for item in self.item_prices_tree.get_children():
            self.item_prices_tree.delete(item)

        items = self.db_manager.search_item(search_query)
        if items:
            for item in items:
                self.item_prices_tree.insert("", tk.END, values=item)

        # Connect search entry 2 to its respective Treeview
        if self.current_window:  # Check if inventory window is open
            search_query_inventory = self.search_entry.get()
            for item in self.info_tree.get_children():
                self.info_tree.delete(item)

            items_inventory = self.db_manager.search_item(search_query_inventory)
            if items_inventory:
                for item in items_inventory:
                    self.info_tree.insert("", tk.END, values=item)

    def show_items(self):
        for item in self.item_prices_tree.get_children():
            self.item_prices_tree.delete(item)

        items = self.db_manager.view_inventory()
        for item in items:
            self.item_prices_tree.insert("", tk.END, values=item)

    def add_items(self):
        add_window = tk.Toplevel(self.master)
        add_window.title("Add Items")
        add_window.geometry("300x300")
        add_window.configure(bg=self.bg_color)

        name_label = tk.Label(add_window, text="Item Name:", bg=self.bg_color, fg=self.text_color, font=("Arial", 10))
        name_label.place(x=10, y=20)
        name_entry = tk.Entry(add_window, bg=self.bg_color, fg=self.text_color, font=("Arial", 10))
        name_entry.place(x=120, y=20)

        quantity_label = tk.Label(add_window, text="Quantity:", bg=self.bg_color, fg=self.text_color, font=("Arial", 10))
        quantity_label.place(x=10, y=60)
        quantity_entry = tk.Entry(add_window, bg=self.bg_color, fg=self.text_color, font=("Arial", 10))
        quantity_entry.place(x=120, y=60)

        price_label = tk.Label(add_window, text="Price:", bg=self.bg_color, fg=self.text_color, font=("Arial", 10))
        price_label.place(x=10, y=100)
        price_entry = tk.Entry(add_window, bg=self.bg_color, fg=self.text_color, font=("Arial", 10))
        price_entry.place(x=120, y=100)

        def add_item_to_db():
            name = name_entry.get()
            quantity = int(quantity_entry.get())
            price = float(price_entry.get())
            self.db_manager.add_item(name, quantity, price)
            add_window.destroy()
            self.show_items()

        add_button = tk.Button(add_window, text="Add", bg=self.button_color, fg=self.text_color_white, font=("Arial", 10), command=add_item_to_db)
        add_button.place(x=120, y=140)

    def delete_item_window(self):
        delete_window = tk.Toplevel(self.master)
        delete_window.title("Delete an Item")
        delete_window.geometry("300x200")
        delete_window.configure(bg=self.bg_color)

        name_label = tk.Label(delete_window, text="Item Name:", bg=self.bg_color, fg=self.text_color, font=("Arial", 10))
        name_label.place(x=10, y=20)
        name_entry = tk.Entry(delete_window, bg=self.bg_color, fg=self.text_color, font=("Arial", 10))
        name_entry.place(x=120, y=20)

        def delete_item_from_db():
            name = name_entry.get()
            self.db_manager.delete_item(name)
            delete_window.destroy()
            self.show_items()

        delete_button = tk.Button(delete_window, text="Delete", bg=self.button_color, fg=self.text_color_white, font=("Arial", 10), command=delete_item_from_db)
        delete_button.place(x=120, y=60)

    def edit_items(self):
        edit_window = tk.Toplevel(self.master)
        edit_window.title("Edit Items")
        edit_window.geometry("300x300")
        edit_window.configure(bg=self.bg_color)

        id_label = tk.Label(edit_window, text="Item ID:", bg=self.bg_color, fg=self.text_color, font=("Arial", 10))
        id_label.place(x=10, y=20)
        id_entry = tk.Entry(edit_window, bg=self.bg_color, fg=self.text_color, font=("Arial", 10))
        id_entry.place(x=120, y=20)

        name_label = tk.Label(edit_window, text="New Name:", bg=self.bg_color, fg=self.text_color, font=("Arial", 10))
        name_label.place(x=10, y=60)
        name_entry = tk.Entry(edit_window, bg=self.bg_color, fg=self.text_color, font=("Arial", 10))
        name_entry.place(x=120, y=60)

        quantity_label = tk.Label(edit_window, text="New Quantity:", bg=self.bg_color, fg=self.text_color, font=("Arial", 10))
        quantity_label.place(x=10, y=100)
        quantity_entry = tk.Entry(edit_window, bg=self.bg_color, fg=self.text_color, font=("Arial", 10))
        quantity_entry.place(x=120, y=100)

        price_label = tk.Label(edit_window, text="New Price:", bg=self.bg_color, fg=self.text_color, font=("Arial", 10))
        price_label.place(x=10, y=140)
        price_entry = tk.Entry(edit_window, bg=self.bg_color, fg=self.text_color, font=("Arial", 10))
        price_entry.place(x=120, y=140)

        def edit_item_in_db():
            item_id = int(id_entry.get())
            name = name_entry.get()
            quantity = int(quantity_entry.get())
            price = float(price_entry.get())
            self.db_manager.edit_item(item_id, name, quantity, price)
            edit_window.destroy()
            self.show_items()

        edit_button = tk.Button(edit_window, text="Edit", bg=self.button_color, fg=self.text_color_white, font=("Arial", 10), command=edit_item_in_db)
        edit_button.place(x=120, y=180)

    def view_inventory(self):
        for item in self.info_tree.get_children():
            self.info_tree.delete(item)

        items = self.db_manager.view_inventory()
        for item in items:
            self.info_tree.insert("", tk.END, values=item)

    def confirm_clear_inventory(self):
        confirm_clear = messagebox.askyesno("Confirm Clear", "Are you sure you want to clear the inventory?")
        if confirm_clear:
            self.db_manager.clear_inventory()
            self.view_inventory()


if __name__ == "__main__":
    root = tk.Tk()
    root.state('zoomed')
    app = GroceryManagementSystem(root)
    root.mainloop()
