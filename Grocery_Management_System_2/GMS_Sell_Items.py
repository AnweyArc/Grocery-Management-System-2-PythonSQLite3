import tkinter as tk
from tkinter import messagebox
import sqlite3

class DatabaseManager:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Create tables for store inventory and sales
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS inventory (
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                quantity INTEGER,
                                price REAL
                            )""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS sales (
                                id INTEGER PRIMARY KEY,
                                items_bought TEXT,
                                total_price REAL
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

    def sell_item(self, item_name, quantity_sold):
        try:
            item = self.get_item_by_name(item_name)
            if item:
                item_id = item[0]
                current_quantity = item[2]
                if current_quantity >= quantity_sold:
                    new_quantity = current_quantity - quantity_sold
                    self.cursor.execute("UPDATE inventory SET quantity=? WHERE id=?", (new_quantity, item_id))
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

    def save_sale(self, items_bought, total_price):
        try:
            self.cursor.execute("INSERT INTO sales (items_bought, total_price) VALUES (?, ?)", (items_bought, total_price))
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error saving sale:", e)

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
        checkout_button = tk.Button(sell_window, text="Add to Cart", bg="#b5485d", fg="white", font=("Arial", 12, "bold"), command=checkout)
        checkout_button.pack(pady=10)

        def bill_out():
            items_bought = self.checkout_result_listbox.get(0, tk.END)
            total_price = sum(float(item.split(":")[-1].split(",")[0].strip()) for item in items_bought)
            items_bought_str = "\n".join(items_bought)
            self.db_manager.save_sale(items_bought_str, total_price)
            self.show_receipt(items_bought, total_price)

        # Bill Out button
        bill_out_button = tk.Button(sell_window, text="Bill Out", bg="#b5485d", fg="white", font=("Arial", 12, "bold"), command=bill_out)
        bill_out_button.pack(pady=10)

    def show_receipt(self, items_bought, total_price):
        receipt_window = tk.Toplevel(self.master)
        receipt_window.title("Receipt")
        receipt_window.geometry("400x500")
        receipt_window.configure(bg="#cabeaf")

        # Receipt title label
        receipt_title_label = tk.Label(receipt_window, text="Receipt", bg="#cabeaf", fg="black", font=("Arial", 20, "bold"))
        receipt_title_label.pack(pady=10)

        # Items bought label
        items_label = tk.Label(receipt_window, text="Items Bought:", bg="#cabeaf", fg="black", font=("Arial", 12))
        items_label.pack(pady=5)

        # Items listbox
        items_listbox = tk.Listbox(receipt_window, bg="#cabeaf", fg="black", font=("Arial", 12))
        for item in items_bought:
            items_listbox.insert(tk.END, item)
        items_listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Total price label
        total_price_label = tk.Label(receipt_window, text=f"Total Price: {total_price}", bg="#cabeaf", fg="black", font=("Arial", 12))
        total_price_label.pack(pady=10)


def main():
    db_manager = DatabaseManager("grocery_database.db")
    root = tk.Tk()
    app = SellItemApp(root, db_manager)
    root.mainloop()

if __name__ == "__main__":
    main()
