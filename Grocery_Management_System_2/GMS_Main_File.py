import tkinter as tk
from tkinter import messagebox
from GMS_Crud import DatabaseManager

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

        # Edit Items Button
        edit_items_button = tk.Button(inventory_window, text="Edit Items", bg=self.button_color, fg=self.text_color_white, font=("Arial", 10, "bold"), command=self.edit_items)
        edit_items_button.place(x=50, y=150, width=130, height=40)

        # View Inventory Button
        view_inventory_button = tk.Button(inventory_window, text="View Inventory", bg=self.button_color, fg=self.text_color_white, font=("Arial", 10, "bold"), command=self.view_inventory)
        view_inventory_button.place(x=50, y=200, width=130, height=40)

        # Clear Inventory Button
        clear_inventory_button = tk.Button(inventory_window, text="Clear Inventory", bg=self.button_color, fg=self.text_color_white, font=("Arial", 10, "bold"), command=self.clear_inventory)
        clear_inventory_button.place(x=50, y=250, width=130, height=40)

        # View Database Button
        view_database_button = tk.Button(inventory_window, text="View Database", bg=self.button_color, fg=self.text_color_white, font=("Arial", 10, "bold"), command=self.view_database)
        view_database_button.place(x=50, y=300, width=130, height=40)

        # Clear Database Button
        clear_database_button = tk.Button(inventory_window, text="Clear Database", bg=self.button_color, fg=self.text_color_white, font=("Arial", 10, "bold"), command=self.clear_database)
        clear_database_button.place(x=50, y=350, width=130, height=40)

        # Listbox on the right side
        self.info_listbox = tk.Listbox(inventory_window, bg=self.bg_color, fg=self.text_color, font=("Arial", 10))
        self.info_listbox.place(x=400, y=100, width=300, height=400)



    def add_items(self):
        # Functionality for Add Items button
        pass

    def edit_items(self):
        # Functionality for Edit Items button
        pass

    def view_inventory(self):
        # Functionality for View Inventory button
        pass

    def clear_inventory(self):
        # Functionality for Clear Inventory button
        pass

    def view_database(self):
        # Functionality for View Database button
        pass

    def clear_database(self):
        # Functionality for Clear Database button
        pass

def main():
    # Main function to initialize the application
    root = tk.Tk()
    app = GroceryManagementSystem(root)
    root.mainloop()

if __name__ == "__main__":
    # Run the main function if the script is executed directly
    main()
