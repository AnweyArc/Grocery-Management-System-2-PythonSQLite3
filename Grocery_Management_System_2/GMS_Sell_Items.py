import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class DatabaseManager:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        try:
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

            # Print schema of the sales table
            self.cursor.execute("PRAGMA table_info(sales)")
            print(self.cursor.fetchall())  # Print the schema of the sales table
        except sqlite3.Error as e:
            print("Error creating tables:", e)

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

    def search_item_by_name(self, item_name):
        try:
            self.cursor.execute("SELECT name, price, quantity FROM inventory WHERE name LIKE ?", ('%' + item_name + '%',))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print("Error searching item by name:", e)
            return []

    def save_sale(self, items_bought, total_price):
        try:
            self.cursor.execute("INSERT INTO sales (items_bought, total_price) VALUES (?, ?)", (items_bought, total_price))
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error saving sale:", e)

    def view_inventory(self):
        try:
            self.cursor.execute("SELECT name, price, quantity FROM inventory")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print("Error viewing inventory:", e)
            return []

    def get_latest_sale_id(self):
        try:
            self.cursor.execute("SELECT MAX(id) FROM sales")
            result = self.cursor.fetchone()
            if result and result[0]:
                return result[0]
            else:
                return 0
        except sqlite3.Error as e:
            print("Error fetching latest sale ID:", e)
            return 0

    def __del__(self):
        self.conn.close()

#------------------------------------------------------------Main Window----------------------------------------------------
class SellItemApp:
    def __init__(self, master, db_manager):
        self.master = master
        self.master.title("Sell Items")
        self.master.configure(bg="#cabeaf")
        self.db_manager = db_manager

        # Fetch the latest sale ID from the database
        self.latest_sale_id = self.db_manager.get_latest_sale_id()

        # Initialize total price variable
        self.total_price = 0

        # Title label
        self.title_label = tk.Label(self.master, text="Sell Items", bg="#cabeaf", fg="black", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=20)

        # Sell item button
        self.sell_item_button = tk.Button(self.master, text="Sell Item", bg="#b5485d", fg="white", font=("Arial", 12, "bold"), command=self.sell_item_window)
        self.sell_item_button.pack(pady=10)

        # Show Stock button
        self.show_stock_button = tk.Button(self.master, text="Show Stock", bg="#b5485d", fg="white", font=("Arial", 12, "bold"), command=self.show_stock)
        self.show_stock_button.pack(pady=10)

        # Search bar
        self.search_entry = tk.Entry(self.master, font=("Arial", 12))
        self.search_entry.pack(pady=10)
        self.search_entry.bind("<KeyRelease>", self.search_inventory)

        self.receipt_treeview = ttk.Treeview(self.master, columns=("Item Name", "Item Price", "Quantity"), show="headings")
        self.receipt_treeview.heading("Item Name", text="Item Name")
        self.receipt_treeview.heading("Item Price", text="Item Price")
        self.receipt_treeview.heading("Quantity", text="Quantity")
        self.receipt_treeview.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)

    def search_inventory(self, event):
        search_term = self.search_entry.get()
        if search_term:
            results = self.db_manager.search_item_by_name(search_term)
        else:
            results = self.db_manager.view_inventory()

        self.receipt_treeview.delete(*self.receipt_treeview.get_children())  # Clear previous items

        for item in results:
            item_name = item[0]
            item_price = item[1]
            item_quantity = item[2]
            self.receipt_treeview.insert("", tk.END, values=(item_name, item_price, item_quantity))

    #------------------------------------------------------------Sell Item Window----------------------------------------------------
    def sell_item_window(self):
        sell_window = tk.Toplevel(self.master)
        sell_window.title("Sell Item")
        sell_window.geometry("900x600")
        sell_window.configure(bg="#cabeaf")

        # Calculate the next sale ID
        self.latest_sale_id += 1

        # Item ID label
        item_id_label = tk.Label(sell_window, text=f"ID: {self.latest_sale_id}", bg="#cabeaf", fg="black", font=("Arial", 12))
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

        # Show Stocks button
        def show_stocks():
            stocks_window = tk.Toplevel(sell_window)
            stocks_window.title("Stocks")
            stocks_window.geometry("700x500")
            stocks_window.configure(bg="#cabeaf")

            stocks_label = tk.Label(stocks_window, text="Stocks", bg="#cabeaf", fg="black", font=("Arial", 20, "bold"))
            stocks_label.pack(pady=10)

            # Search bar
            search_entry = tk.Entry(stocks_window, font=("Arial", 12))
            search_entry.pack(pady=10)

            # Create Treeview for tabular display
            tree = ttk.Treeview(stocks_window, columns=("Item Name", "Item Price", "Quantity Left"), show="headings")
            tree.heading("Item Name", text="Item Name")
            tree.heading("Item Price", text="Item Price")
            tree.heading("Quantity Left", text="Quantity Left")
            tree.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)

            def search_inventory(event):
                search_term = search_entry.get()
                if search_term:
                    results = self.db_manager.search_item_by_name(search_term)
                else:
                    results = self.db_manager.view_inventory()

                # Clear previous items in the tree
                for item in tree.get_children():
                    tree.delete(item)

                for item in results:
                    item_name = item[0]
                    item_price = item[1]
                    item_quantity = item[2]
                    tree.insert("", tk.END, values=(item_name, item_price, item_quantity))

            search_entry.bind("<KeyRelease>", search_inventory)

            # Load initial data
            search_inventory(None)

        show_stocks_button = tk.Button(sell_window, text="Show Stocks", bg="#b5485d", fg="white", font=("Arial", 12, "bold"), command=show_stocks)
        show_stocks_button.pack(pady=10)

        # Checkout result listbox
        self.checkout_result_listbox = tk.Listbox(sell_window, bg="#cabeaf", fg="black", font=("Arial", 12))
        self.checkout_result_listbox.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)

        def checkout():
            item_name = item_name_entry.get()
            item_quantity = int(item_quantity_entry.get())

            # Fetch item price and remaining quantity after selling
            success, item_price, remaining_quantity = self.db_manager.sell_item(item_name, item_quantity)

            if success:
                total_price = item_quantity * item_price
                self.total_price += total_price  # Update the total price
                if remaining_quantity is not None:
                    message = f"Item Name: {item_name:<20} Price per Item: {item_price:<15} Quantity: {item_quantity:<15} Total Price: {total_price:<15} Item Left: {remaining_quantity:<10}"
                else:
                    message = f"Item Name: {item_name:<20} Price per Item: {item_price:<15} Quantity: {item_quantity:<15} Total Price: {total_price:<15}"
                self.checkout_result_listbox.insert(tk.END, message)
            else:
                messagebox.showerror("Error", item_price)

        # Checkout button
        checkout_button = tk.Button(sell_window, text="Add to Cart", bg="#b5485d", fg="white", font=("Arial", 12, "bold"), command=checkout)
        checkout_button.pack(pady=10)

        def bill_out():
            items_bought = self.checkout_result_listbox.get(0, tk.END)
            total_price = self.total_price  # Use the instance variable total price
            self.db_manager.save_sale("\n".join(items_bought), total_price)
            self.show_receipt(items_bought, total_price)

        # Bill Out button
        bill_out_button = tk.Button(sell_window, text="Bill Out", bg="#b5485d", fg="white", font=("Arial", 12, "bold"), command=bill_out)
        bill_out_button.pack(pady=10)

    def show_receipt(self, items_bought, total_price):
        receipt_window = tk.Toplevel(self.master)
        receipt_window.title("Receipt")
        receipt_window.geometry("900x600")
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

        # Money entry
        money_label = tk.Label(receipt_window, text="Enter Money:", bg="#cabeaf", fg="black", font=("Arial", 12))
        money_label.pack(pady=5)
        money_entry = tk.Entry(receipt_window, font=("Arial", 12))
        money_entry.pack(pady=5)

        # Calculate button
        def calculate_change():
            try:
                money = float(money_entry.get())
                change = money - total_price
                change_label.config(text=f"Change: {change}")
            except ValueError:
                messagebox.showerror("Error", "Invalid input for money.")

        calculate_button = tk.Button(receipt_window, text="Calculate Change", bg="#b5485d", fg="white", font=("Arial", 12, "bold"), command=calculate_change)
        calculate_button.pack(pady=10)

        # Change label
        change_label = tk.Label(receipt_window, text="Change:", bg="#cabeaf", fg="black", font=("Arial", 12))
        change_label.pack(pady=10)

        # Finish session button
        def finish_session():
            receipt_window.destroy()
            messagebox.showinfo("Thank You", "Thank you for buying!")

        finish_button = tk.Button(receipt_window, text="Finish Session", bg="#b5485d", fg="white", font=("Arial", 12, "bold"), command=finish_session)
        finish_button.pack(pady=10)

    def show_stock(self):
        # Clear previous items
        self.receipt_treeview.delete(*self.receipt_treeview.get_children())

        inventory_items = self.db_manager.view_inventory()

        for item in inventory_items:
            item_name = item[0]
            item_price = item[1]
            item_quantity = item[2]
            # Insert each item into the treeview with correct values
            self.receipt_treeview.insert("", tk.END, values=(item_name, item_price, item_quantity))

def main():
    db_manager = DatabaseManager("grocery_database.db")
    root = tk.Tk()
    root.state("zoomed")
    app = SellItemApp(root, db_manager)
    root.mainloop()

if __name__ == "__main__":
    main()
