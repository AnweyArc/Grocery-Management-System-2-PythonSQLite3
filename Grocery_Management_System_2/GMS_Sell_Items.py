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
                                    FOREIGN KEY (item_id) REFERENCES inventory(id)
                                )""")
        

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS sales (
                        id INTEGER PRIMARY KEY,
                        item_id INTEGER,
                        item_name TEXT,
                        quantity_sold INTEGER,
                        sale_date TEXT,
                        FOREIGN KEY (item_id) REFERENCES inventory(id)
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

    def sell_item(self, item_name, quantity_sold):
        try:
            item = self.get_item_by_name(item_name)
            if item:
                item_id = item[0]
                current_quantity = item[2]
                if current_quantity >= quantity_sold:
                    new_quantity = current_quantity - quantity_sold
                    self.cursor.execute("UPDATE inventory SET quantity=? WHERE id=?", (new_quantity, item_id))
                    # Get the item name from the inventory and insert it into the sales table
                    item_name = item[1]
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

    def get_item_by_name(self, item_name):
        try:
            self.cursor.execute("SELECT * FROM inventory WHERE name=?", (item_name,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print("Error getting item by name:", e)
            return None
    
    def __del__(self):
        self.conn.close()


class SellItemApp:
    def __init__(self, master, db_manager):
        self.master = master
        self.master.title("Sell Items")
        self.master.geometry("800x600")
        self.master.configure(bg="#cabeaf")
        self.db_manager = db_manager

        # Title label
        self.title_label = tk.Label(self.master, text="Sell Items", bg="#cabeaf", fg="black", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=20)

        # Sell item button
        self.sell_item_button = tk.Button(self.master, text="Sell Item", bg="#b5485d", fg="white", font=("Arial", 12, "bold"), command=self.sell_item_window)
        self.sell_item_button.pack(pady=10)

        # Print receipt button
        self.print_receipt_button = tk.Button(self.master, text="Print Receipt", bg="#b5485d", fg="white", font=("Arial", 12, "bold"))
        self.print_receipt_button.pack(pady=10)

        # Receipt listbox
        self.receipt_listbox = tk.Listbox(self.master, bg="#cabeaf", fg="black", font=("Arial", 12))
        self.receipt_listbox.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)

    def sell_item_window(self):
        sell_window = tk.Toplevel(self.master)
        sell_window.title("Sell Item")
        sell_window.geometry("500x600")
        sell_window.configure(bg="#cabeaf")

        # Item ID label
        item_id_label = tk.Label(sell_window, text="ID: 1", bg="#cabeaf", fg="black", font=("Arial", 12))
        item_id_label.pack(pady=10)

        # Item Name entry
        item_name_label = tk.Label(sell_window, text="Item Name:", bg="#cabeaf", fg="black", font=("Arial", 12))
        item_name_label.pack(pady=5)
        item_name_entry = tk.Entry(sell_window, font=("Arial", 12))
        item_name_entry.pack(pady=5)

        # Item Quantity entry
        item_quantity_label = tk.Label(sell_window, text="Item Quantity:", bg="#cabeaf", fg="black", font=("Arial", 12))
        item_quantity_label.pack(pady=5)
        item_quantity_entry = tk.Entry(sell_window, font=("Arial", 12))
        item_quantity_entry.pack(pady=5)

        # Checkout result listbox
        self.checkout_result_listbox = tk.Listbox(sell_window, bg="#cabeaf", fg="black", font=("Arial", 12))
        self.checkout_result_listbox.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)

        def checkout():
            item_name = item_name_entry.get()
            item_quantity = int(item_quantity_entry.get())
            success, item_price, remaining_quantity = self.db_manager.sell_item(item_name, item_quantity)
            if success:
                total_price = item_price * item_quantity
                if remaining_quantity is not None:
                    message = f"Item Name: {item_name}, Price per Item: {item_price}, Quantity: {item_quantity}, Total Price: {total_price} -- Item Left: {remaining_quantity}"
                else:
                    message = f"Item Name: {item_name}, Price per Item: {item_price}, Quantity: {item_quantity}, Total Price: {total_price}"
                self.checkout_result_listbox.insert(tk.END, message)
            else:
                messagebox.showerror("Error", item_price)

        # Checkout button
        checkout_button = tk.Button(sell_window, text="Checkout", bg="#b5485d", fg="white", font=("Arial", 12, "bold"), command=checkout)
        checkout_button.pack(pady=10)


def main():
    db_manager = DatabaseManager("grocery_database.db")
    root = tk.Tk()
    app = SellItemApp(root, db_manager)
    root.mainloop()

if __name__ == "__main__":
    main()
