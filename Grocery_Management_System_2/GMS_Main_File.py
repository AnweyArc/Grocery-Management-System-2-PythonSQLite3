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

        #SearchEntry1
        self.item_prices_entry = tk.Entry(self.master, bg=self.bg_color, fg=self.text_color, font=("Arial", 10))
        self.item_prices_entry.place(x=704, y=220, width=140)
        self.item_prices_entry.bind("<KeyRelease>", self.search_items)
        #Listbox1
        self.item_prices_listbox = tk.Listbox(self.master, bg=self.bg_color, fg=self.text_color, font=("Arial", 10))
        self.item_prices_listbox.place(x=580, y=250, width=380, height=200)

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
        
        # Listbox2
        self.info_listbox = tk.Listbox(inventory_window, bg=self.bg_color, fg=self.text_color, font=("Arial", 10))
        self.info_listbox.place(x=280, y=100, width=600, height=400)

        self.current_window = inventory_window

    def search_items(self, event=None):
        search_query = self.item_prices_entry.get()
        self.item_prices_listbox.delete(0, tk.END)  # Clear previous items

        items = self.db_manager.search_item(search_query)
        if items:
            self.item_prices_listbox.insert(tk.END, "{:<20} {:<15} {:<15}".format("Item Name", "Item Price", "Quantity Left"))
            for item in items:
                item_str = "{:<20} {:<15} {:<15}".format(item[0], item[1], item[2])
                self.item_prices_listbox.insert(tk.END, item_str)

        # Connect search entry 2 to its respective listbox
        if self.current_window:  # Check if inventory window is open
            search_query_2 = self.search_entry.get()
            if search_query_2:  # Check if the search query is not empty
                items_2 = self.db_manager.search_item(search_query_2)
                if items_2:
                    self.info_listbox.delete(0, tk.END)  # Clear previous items
                    self.info_listbox.insert(tk.END, "{:<20} {:<15} {:<15}".format("Item Name", "Item Price", "Quantity Left"))
                    for item in items_2:
                        item_str = "{:<20} {:<15} {:<15}".format(item[0], item[1], item[2])
                        self.info_listbox.insert(tk.END, item_str)
                else:
                    self.info_listbox.delete(0, tk.END)  # Clear previous items
                    self.info_listbox.insert(tk.END, "Item not found")

    def show_items(self):
        # Fetch and display items in the item prices listbox
        self.item_prices_listbox.delete(0, tk.END)  # Clear previous items
        
        inventory_items = self.db_manager.view_inventory()
        
        # Add headers
        self.item_prices_listbox.insert(tk.END, "{:<20} {:<15} {:<15}".format("Item Name", "Item Price", "Quantity Left"))
        
        for item in inventory_items:
            item_name = item[0]
            item_price = item[1]
            item_quantity = item[2]
            # Format each item to align properly in columns
            item_str = "{:<20} {:<15} {:<15}".format(item_name, item_price, item_quantity)
            self.item_prices_listbox.insert(tk.END, item_str)

    def add_items(self):
        def add_new_item_to_database():
            item_name = new_item_name_entry.get()
            item_quantity = new_item_quantity_entry.get()
            item_price = new_item_price_entry.get()
            
            # Check if any field is empty
            if not item_name or not item_quantity or not item_price:
                messagebox.showerror("Error", "No input! Please enter values!")
                return
            
            try:
                item_quantity = int(item_quantity)
                item_price = float(item_price)
            except ValueError:
                messagebox.showerror("Error", "Invalid input! Quantity should be an integer and Price should be a number.")
                return
        
            self.db_manager.add_item(item_name, item_quantity, item_price)
            add_window.destroy()
            # Ask if the user wants to add another item
            if messagebox.askyesno("Add Another Item", "Do you want to add another item?"):
                self.add_items()  # Recursively call add_items to add another item

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
            item_quantity = existing_item_quantity_entry.get()

            # Check if any field is empty
            if not item_name or not item_quantity:
                messagebox.showerror("Error", "No input! Please enter values!")
                return
            
            try:
                item_quantity = int(item_quantity)
            except ValueError:
                messagebox.showerror("Error", "Invalid input! Quantity should be an integer.")
                return

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

    def delete_item_window(self):
        delete_window = tk.Toplevel(self.master)
        delete_window.title("Delete Item")

        delete_item_frame = tk.LabelFrame(delete_window, text="Delete Item")
        delete_item_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        delete_item_name_label = tk.Label(delete_item_frame, text="Item Name:")
        delete_item_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        delete_item_name_entry = tk.Entry(delete_item_frame)
        delete_item_name_entry.grid(row=0, column=1, padx=10, pady=5)

        def delete_item_from_database():
            item_name = delete_item_name_entry.get()
            self.db_manager.delete_item(item_name)
            delete_window.destroy()
            self.view_inventory()

        delete_item_button = tk.Button(delete_item_frame, text="Delete Item", command=delete_item_from_database)
        delete_item_button.grid(row=1, column=0, columnspan=2, pady=10)

    def edit_items(self):
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

        new_price_label = tk.Label(edit_window, text="New Price/Item:")
        new_price_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        new_price_entry = tk.Entry(edit_window)
        new_price_entry.grid(row=3, column=1, padx=10, pady=5)

        def update_item_in_database():
            item_name = item_name_entry.get()
            new_name = new_name_entry.get()
            new_quantity = new_quantity_entry.get()
            new_price = new_price_entry.get()

            # Check if any field is empty
            if not item_name or not new_name or not new_quantity or not new_price:
                messagebox.showerror("Error", "No input! Please enter values!")
                return
            
            try:
                new_quantity = int(new_quantity)
                new_price = float(new_price)
            except ValueError:
                messagebox.showerror("Error", "Invalid input! Quantity should be an integer and Price should be a number.")
                return

            item = self.db_manager.get_item_by_name(item_name)
            if item:
                self.db_manager.edit_item(item[0], new_name, new_quantity, new_price)
                edit_window.destroy()
                self.view_inventory()
            else:
                messagebox.showerror("Item Not Found", "The item does not exist in the database.")

        edit_item_button = tk.Button(edit_window, text="Edit Item", command=update_item_in_database)
        edit_item_button.grid(row=4, column=0, columnspan=2, pady=10)

    def confirm_clear_inventory(self):
        response = messagebox.askyesno("Confirm", "Do you want to clear the entire inventory?")
        if response:
            self.db_manager.clear_inventory()
            self.view_inventory()

    def view_inventory(self):
        inventory_items = self.db_manager.view_inventory()
        self.info_listbox.delete(0, tk.END)  # Clear previous items

        if inventory_items:
            self.info_listbox.insert(tk.END, "{:<20} {:<15} {:<15}".format("Item Name", "Item Price", "Quantity Left"))
            for item in inventory_items:
                item_name = item[0]
                item_price = item[1]
                item_quantity = item[2]
                item_str = "{:<20} {:<15} {:<15}".format(item_name, item_price, item_quantity)
                self.info_listbox.insert(tk.END, item_str)
        else:
            self.info_listbox.insert(tk.END, "Inventory is empty")


def main():
    root = tk.Tk()
    app = GroceryManagementSystem(root)
    root.state('zoomed')
    root.mainloop()

if __name__ == "__main__":
    main()
