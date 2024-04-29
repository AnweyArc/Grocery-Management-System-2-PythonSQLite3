import tkinter as tk
from tkinter import messagebox
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
                                item_name TEXT,
                                quantity_sold INTEGER,
                                sale_date TEXT,
                                FOREIGN KEY (item_id) REFERENCES inventory(id)
                            )""")  # Added "item_name" column

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

    # Edit Items
    def edit_item(self, item_id, new_name, new_quantity, new_price):
        try:
            self.cursor.execute("UPDATE inventory SET name=?, quantity=?, price=? WHERE id=?",
                                (new_name, new_quantity, new_price, item_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error editing item:", e)

    def get_item_by_name(self, item_name):
        try:
            self.cursor.execute("SELECT * FROM inventory WHERE name=?", (item_name,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print("Error getting item by name:", e)
            return None
    
    def delete_item(self, item_name):
        try:
            self.cursor.execute("DELETE FROM inventory WHERE name=?", (item_name,))
            self.conn.commit()
            print("Item deleted successfully.")
        except sqlite3.Error as e:
            print("Error deleting item:", e)

    # Sales methods
    def sell_item(self, item_name, quantity_sold):
        try:
            item = self.get_item_by_name(item_name)
            if item:
                item_id = item[0]
                current_quantity = item[2]
                if current_quantity >= quantity_sold:
                    new_quantity = current_quantity - quantity_sold
                    self.cursor.execute("UPDATE inventory SET quantity=? WHERE id=?", (new_quantity, item_id))
                    self.cursor.execute("INSERT INTO sales (item_id, item_name, quantity_sold) VALUES (?, ?, ?)", (item_id, item_name, quantity_sold))
                    self.conn.commit()
                    return True, item[3], new_quantity  # Return True, item price, and new quantity
                else:
                    return False, f"Sorry! Only {current_quantity} items left!", None
            else:
                return False, "Sorry, out of stock", None
        except sqlite3.Error as e:
            print("Error selling item:", e)
            return False, "An error occurred", None

    def __del__(self):
        self.conn.close()


class GroceryManagementSystem:
    def __init__(self, master):
        # Initialize the main window
        self.master = master
        self.master.title("Grocery Management System")
        self.master.geometry("800x600")  # Set window size to 800x600
        self.db_manager = DatabaseManager("grocery_database.db")

        # Color Palette
        self.bg_color = "#cabeaf"
        self.button_color = "#b5485d"
        self.text_color = "black"
        self.text_color_white = "white"

        # Configure Background
        self.master.configure(bg=self.bg_color)

        # Title text
        self.title_label = tk.Label(self.master, text="Grocery Management System", bg=self.bg_color, fg=self.text_color, font=("Arial", 20, "bold"))
        self.title_label.place(x=210, y=20)  # Manual positioning

        # Buttons
        self.sell_button = tk.Button(self.master, text="Sell Items", bg=self.button_color, fg=self.text_color_white, font=("Arial", 12, "bold"), command=self.open_sell_window)
        self.sell_button.place(x=230, y=80, width=150, height=30)  # Manual positioning

        self.store_inventory_button = tk.Button(self.master, text="Store Inventory", bg=self.button_color, fg=self.text_color_white, font=("Arial", 12, "bold"), command=self.open_inventory_window)
        self.store_inventory_button.place(x=420, y=80, width=150, height=30)  # Manual positioning

        # Listbox
        # Label
        self.item_prices_label = tk.Label(self.master, text="Item Prices", bg=self.bg_color, fg=self.text_color, font=("Arial", 12, "bold"))
        self.item_prices_label.place(x=356, y=140)  # Manual positioning
        # Search Box
        self.item_prices_entry = tk.Entry(self.master, bg=self.bg_color, fg=self.text_color, font=("Arial", 10))
        self.item_prices_entry.place(x=330, y=170, width=140)  # Manual positioning
        # ListBox
        self.item_prices_listbox = tk.Listbox(self.master, bg=self.bg_color, fg=self.text_color, font=("Arial", 10))
        self.item_prices_listbox.place(x=230, y=200, width=340, height=200)  # Manual positioning

    def open_sell_window(self):
        # Function to open the "Sell Items" window
        sell_window = tk.Toplevel(self.master)
        sell_window.title("Sell Items")
        sell_window.geometry("800x600")
        sell_window.configure(bg=self.bg_color)

        # Title text for Sell Items window
        title_label = tk.Label(sell_window, text="Sell Items", bg=self.bg_color, fg="black", font=("Arial", 20, "bold"))
        title_label.place(x=320, y=20)

    def open_inventory_window(self):
        # Function to open the "Store Inventory" window
        inventory_window = tk.Toplevel(self.master)
        inventory_window.title("Store Inventory")
        inventory_window.geometry("800x600")
        inventory_window.configure(bg=self.bg_color)

        # Title text for Store Inventory window
        title_label = tk.Label(inventory_window, text="Store Inventory", bg=self.bg_color, fg="black", font=("Arial", 20, "bold"))
        title_label.place(x=290, y=20)

        # Add Items Button
        add_items_button = tk.Button(inventory_window, text="Add Items", bg=self.button_color, fg=self.text_color_white, font=("Arial", 10, "bold"), command=self.add_items)
        add_items_button.place(x=50, y=100, width=130, height=40)

        # Delete Item Button
        delete_item_button = tk.Button(inventory_window, text="Delete Item", bg=self.button_color, fg=self.text_color_white, font=("Arial", 10, "bold"), command=self.delete_item)
        delete_item_button.place(x=50, y=150, width=130, height=40)

        # Edit Items Button
        edit_items_button = tk.Button(inventory_window, text="Edit Items", bg=self.button_color, fg=self.text_color_white, font=("Arial", 10, "bold"), command=self.edit_items)
        edit_items_button.place(x=50, y=200, width=130, height=40)

        # View Inventory Button
        view_inventory_button = tk.Button(inventory_window, text="View Inventory", bg=self.button_color, fg=self.text_color_white, font=("Arial", 10, "bold"), command=self.view_inventory)
        view_inventory_button.place(x=50, y=250, width=130, height=40)

        # Clear Inventory Button
        clear_inventory_button = tk.Button(inventory_window, text="Clear Inventory", bg=self.button_color, fg=self.text_color_white, font=("Arial", 10, "bold"), command=self.clear_inventory)
        clear_inventory_button.place(x=50, y=300, width=130, height=40)

        # Listbox on the right side
        self.info_listbox = tk.Listbox(inventory_window, bg=self.bg_color, fg=self.text_color, font=("Arial", 10))
        self.info_listbox.place(x=400, y=100, width=300, height=400)

    def add_items(self):
        # Functionality for Add Items button
        add_window = tk.Toplevel(self.master)
        add_window.title("Add Item")

        new_item_frame = tk.LabelFrame(add_window, text="Add New Item")
        new_item_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        new_item_name_label = tk.Label(new_item_frame, text="Item Name:")
        new_item_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        new_item_name_entry = tk.Entry(new_item_frame)
        new_item_name_entry.grid(row=0, column=1, padx=10, pady=5)

        new_item_quantity_label = tk.Label(new_item_frame, text="Item Quantity:")
        new_item_quantity_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        new_item_quantity_entry = tk.Entry(new_item_frame)
        new_item_quantity_entry.grid(row=1, column=1, padx=10, pady=5)

        new_item_price_label = tk.Label(new_item_frame, text="Price/Item:")
        new_item_price_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        new_item_price_entry = tk.Entry(new_item_frame)
        new_item_price_entry.grid(row=2, column=1, padx=10, pady=5)

        def add_new_item_to_database():
            item_name = new_item_name_entry.get()
            item_quantity = int(new_item_quantity_entry.get())
            item_price = float(new_item_price_entry.get())
            self.db_manager.add_item(item_name, item_quantity, item_price)
            add_window.destroy()
            # Refresh the inventory view
            self.view_inventory()

        add_new_item_button = tk.Button(new_item_frame, text="Add New Item", command=add_new_item_to_database)
        add_new_item_button.grid(row=3, column=0, columnspan=2, pady=10)

        existing_item_frame = tk.LabelFrame(add_window, text="Add Existing Item")
        existing_item_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        existing_item_name_label = tk.Label(existing_item_frame, text="Item Name:")
        existing_item_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        existing_item_name_entry = tk.Entry(existing_item_frame)
        existing_item_name_entry.grid(row=0, column=1, padx=10, pady=5)

        existing_item_quantity_label = tk.Label(existing_item_frame, text="Item Quantity:")
        existing_item_quantity_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        existing_item_quantity_entry = tk.Entry(existing_item_frame)
        existing_item_quantity_entry.grid(row=1, column=1, padx=10, pady=5)

        def add_existing_item_to_database():
            item_name = existing_item_name_entry.get()
            item_quantity = int(existing_item_quantity_entry.get())
            item = self.db_manager.get_item_by_name(item_name)
            if item:
                current_quantity = item[2]
                new_quantity = current_quantity + item_quantity
                self.db_manager.edit_item(item[0], item[1], new_quantity, item[3])
                add_window.destroy()
                self.view_inventory()
            else:
                messagebox.showerror("Item Not Found", "The item does not exist in the database.")

        add_existing_item_button = tk.Button(existing_item_frame, text="Add Existing Item", command=add_existing_item_to_database)
        add_existing_item_button.grid(row=2, column=0, columnspan=2, pady=10)


    def edit_items(self):
        # Functionality for Edit Items button
        edit_window = tk.Toplevel(self.master)
        edit_window.title("Edit Item")

        item_name_label = tk.Label(edit_window, text="Item Name:")
        item_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        item_name_entry = tk.Entry(edit_window)
        item_name_entry.grid(row=0, column=1, padx=10, pady=5)

        new_name_label = tk.Label(edit_window, text="New Item Name:")
        new_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        new_name_entry = tk.Entry(edit_window)
        new_name_entry.grid(row=1, column=1, padx=10, pady=5)

        new_quantity_label = tk.Label(edit_window, text="New Quantity:")
        new_quantity_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        new_quantity_entry = tk.Entry(edit_window)
        new_quantity_entry.grid(row=2, column=1, padx=10, pady=5)

        new_price_label = tk.Label(edit_window, text="New Price:")
        new_price_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        new_price_entry = tk.Entry(edit_window)
        new_price_entry.grid(row=3, column=1, padx=10, pady=5)

        def apply_edit():
            item_name = item_name_entry.get()
            new_name = new_name_entry.get()
            new_quantity = int(new_quantity_entry.get())
            new_price = float(new_price_entry.get())
            item = self.db_manager.get_item_by_name(item_name)
            if item:
                item_id = item[0]
                self.db_manager.edit_item(item_id, new_name, new_quantity, new_price)
                edit_window.destroy()
                # Refresh the view by calling view_inventory
                self.view_inventory()
            else:
                messagebox.showerror("Item Not Found", "The item does not exist in the inventory.")

        apply_button = tk.Button(edit_window, text="Apply Edit", command=apply_edit)
        apply_button.grid(row=4, column=0, columnspan=2, pady=10)


    def view_inventory(self):
        # Functionality for View Inventory button
        self.info_listbox.delete(0, tk.END)  # Clear the listbox
        inventory_items = self.db_manager.view_inventory()
        if inventory_items:
            for item in inventory_items:
                item_name = item[0]
                item_price = item[1]  # corrected index for price
                item_quantity = item[2]  # corrected index for quantity
                self.info_listbox.insert(tk.END, f"Item Name: {item_name}\n Item Price: {item_price}\n Quantity Left: {item_quantity}")
        else:
            self.info_listbox.insert(tk.END, "No items on the inventory!")

    def delete_item(self):
        # Functionality for Delete Item button
        delete_window = tk.Toplevel(self.master)
        delete_window.title("Delete Item")

        item_name_label = tk.Label(delete_window, text="Item Name:")
        item_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        item_name_entry = tk.Entry(delete_window)
        item_name_entry.grid(row=0, column=1, padx=10, pady=5)

        def delete_item_from_inventory():
            item_name = item_name_entry.get()
            self.db_manager.delete_item(item_name)
            delete_window.destroy()
            # Refresh the inventory view
            self.view_inventory()

        delete_button = tk.Button(delete_window, text="Delete Item", command=delete_item_from_inventory)
        delete_button.grid(row=1, column=0, columnspan=2, pady=10)

    def clear_inventory(self):
        # Functionality for Clear Inventory button
        self.db_manager.clear_inventory()
        self.info_listbox.delete(0, tk.END)  # Clear the listbox
        self.info_listbox.insert(tk.END, "Inventory Cleared!")

def main():
    # Main function to initialize the application
    root = tk.Tk()
    app = GroceryManagementSystem(root)
    root.mainloop()

if __name__ == "__main__":
    # Run the main function if the script is executed directly
    main()
