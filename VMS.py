import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import re

class VisitorManagementSystem:
    def __init__(self, root, db_file):
        self.root = root
        self.root.title("Visitor Management System")
        self.visitor_tree = None
        self.create_admin_widgets()
        self.delete_visitor()

        # Create a custom style for the buttons
        style = ttk.Style()
        style.configure("Custom.TButton", font=("Bahnschrift", 20, "bold"), padding=10)

        # Database connection
        self.conn = sqlite3.connect(db_file)
        self.create_table()

        # Variables to store user input
        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.office_var = tk.StringVar()

        # Admin login variables
        self.admin_username_var = tk.StringVar()
        self.admin_password_var = tk.StringVar()

        # Create and set up widgets for visitor registration
        self.create_registration_widgets()

        # Create and set up widgets for admin login
        self.create_admin_login_widgets()
        

    def create_table(self):
        # Create 'visitors' table if not exists
        query = '''
        CREATE TABLE IF NOT EXISTS visitors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        office TEXT NOT NULL,
        in_time TEXT,
        date TEXT
        )
        '''
        self.conn.execute(query)
        self.conn.commit()

    def create_registration_widgets(self):
        registration_frame = ttk.Frame(self.root)
        registration_frame.pack(pady=10)

        # Label for the registration page
        ttk.Label(registration_frame, text="Visitor Registration",font=("Bahnschrift", 30, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Labels and Entry widgets for user input
        ttk.Label(registration_frame, text="Name:",font=("Bahnschrift", 15, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        name_entry = ttk.Entry(registration_frame,font=("Bahnschrift", 15, "bold"),textvariable=self.name_var)
        name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(registration_frame, text="Phone:",font=("Bahnschrift", 15, "bold")).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        phone_entry = ttk.Entry(registration_frame, textvariable=self.phone_var,font=("Bahnschrift", 15, "bold"))
        phone_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(registration_frame, text="Office:",font=("Bahnschrift", 15, "bold")).grid(row=3, column=0, padx=5, pady=5, sticky="e")
        office_entry = ttk.Entry(registration_frame, textvariable=self.office_var,font=("Bahnschrift", 15, "bold"))
        office_entry.grid(row=3, column=1, padx=5, pady=5)

        # Button to submit the registration
        ttk.Button(registration_frame,text="Submit", style="Custom.TButton",command=self.submit_registration).grid(row=4, column=0, columnspan=2, pady=10)

        name_entry.config(validate="key", validatecommand=(name_entry.register(self.validate_name), "%P"))
        phone_entry.config(validate="key", validatecommand=(phone_entry.register(self.validate_phone), "%P"))

    def validate_name(self, name):

         # Validate name format (no special characters)
        if re.match(r'^[a-zA-Z\s]*$', name):
            return True
        else:
            return False
       
        if len(name) <= 20:
            return True
        else:
            return False

    def validate_phone(self, phone):
        # Validate phone number format (10 digits)
        if re.match(r'^\d{0,10}$', phone):
            return True
        else:
            return False


    def submit_registration(self):
        # Retrieve user input
        name = self.name_var.get()
        phone = self.phone_var.get()
        office = self.office_var.get()

        # Validate if all fields are filled
        if name == '' or phone == '' or office == '':
            messagebox.showerror("Error", "Please fill in all fields.")
        else:
            # Insert data into the database
            in_time = datetime.now().strftime("%H:%M:%S")
            date = datetime.now().strftime("%Y-%m-%d")
            query = "INSERT INTO visitors (name, phone, office, in_time, date) VALUES (?, ?, ?, ?, ?)"
            self.conn.execute(query, (name, phone, office, in_time, date))
            self.conn.commit()

            # Display a message with the registration details
            message = f"Registration Successful!\nName: {name}\nPhone: {phone}\nOffice: {office}"
            messagebox.showinfo("Success", message)

            # Clear the input fields
            self.name_var.set('')
            self.phone_var.set('')
            self.office_var.set('')

    def create_admin_login_widgets(self):
        admin_frame = ttk.Frame(self.root)
        admin_frame.pack(pady=10)

        # Label for the admin login page
        ttk.Label(admin_frame, text="Admin Login",font=("Bahnschrift", 30, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Labels and Entry widgets for admin login
        ttk.Label(admin_frame, text="Username:",font=("Bahnschrift", 15, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        username_entry = ttk.Entry(admin_frame, textvariable=self.admin_username_var,font=("Bahnschrift", 15, "bold"))
        username_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(admin_frame, text="Password:",font=("Bahnschrift", 15, "bold")).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        password_entry = ttk.Entry(admin_frame, textvariable=self.admin_password_var, show="*",font=("Bahnschrift", 15, "bold"))
        password_entry.grid(row=2, column=1, padx=5, pady=5)

        # Button to login as admin
        ttk.Button(admin_frame, text="Login", style="Custom.TButton",command=self.admin_login).grid(row=3, column=0, columnspan=2, pady=10)

      

    def admin_login(self):
        # Check if username and password are correct
        if self.admin_username_var.get() == "admin" and self.admin_password_var.get() == "password":
            # Successful login, show admin page
            self.show_admin_page()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def show_admin_page(self):
        # Destroy registration widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create and set up widgets for admin page
        admin_frame = ttk.Frame(self.root)
        admin_frame.pack(pady=10)

        # Label for the admin page
        ttk.Label(admin_frame, text="Admin Page",font=("Bahnschrift", 30, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Button to view visitor data
        ttk.Button(admin_frame, text="View Visitor Data",style="Custom.TButton", command=self.view_visitor_data).grid(row=1, column=0, padx=5, pady=5)

        # Button to delete selected visitor
        ttk.Button(admin_frame, text="Delete Selected", style="Custom.TButton",command=self.delete_visitor).grid(row=1, column=1, padx=5, pady=5)

        # Button to go back to the registration page
        ttk.Button(admin_frame, text="Back to Registration",style="Custom.TButton", command=self.show_registration_page).grid(row=2, column=0, columnspan=2, pady=10)

    def view_visitor_data(self):
        # Create a new window for displaying visitor data
        visitor_data_window = tk.Toplevel(self.root)
        visitor_data_window.title("Visitor Data")

        # Treeview for displaying visitor data
        tree = ttk.Treeview(visitor_data_window, columns=("ID", "Name", "Phone", "Office", "In-Time", "Date"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Phone", text="Phone")
        tree.heading("Office", text="Office")
        tree.heading("In-Time", text="In-Time")
        tree.heading("Date", text="Date")

        # Populate treeview with data from the database
        data = self.fetch_data_from_db()
        for row in data:
            tree.insert("", "end", values=row)

        tree.pack(padx=10, pady=10)

     

    def fetch_data_from_db(self):
        # Fetch all data from the 'visitors' table
        query = "SELECT * FROM visitors"
        cursor = self.conn.execute(query)
        return cursor.fetchall()

    def create_admin_widgets(self):
        self.visitor_tree = ttk.Treeview(self.root, columns=("ID", "Name", "Phone"))

    def delete_visitor(self):
        if self.visitor_tree is None:
            print("Visitor tree not initialized.")
            return
 
        selected_item = self.visitor_tree.selection()
	# Get the selected item from the treeview
             
        if not selected_item:
            messagebox.showerror("Error", "Please select a visitor to delete.")
            return
        # Assuming selected_id is extracted from the selected_item
        selected_id = self.visitor_tree.item(selected_item, "values")[0]
        if not selected_id:
            messagebox.showerror("Error", "Invalid selection.")
            return
        # Get the ID of the selected item
        selected_item = self.visitor_tree.item(selected_item, "values")[0]
        confirm_delete = messagebox.askyesno("Confirmation", "Are you sure you want to delete this visitor?")
        if confirm_delete:
            # Delete the selected entry from the database
            query = f"DELETE FROM visitors WHERE id={selected_id}"
            self.conn.execute(query)
            self.conn.commit()

            # Delete the selected item from the treeview
            self.visitor_tree.delete(selected_item)
            messagebox.showinfo("Success", "Visitor deleted successfully.")

   

    def show_registration_page(self):
        # Destroy admin widgets and recreate registration widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_registration_widgets()

if __name__ == "__main__":
    # Specify the path to your SQLite database file
    db_file_path = "visitor_management.db"

    root = tk.Tk()
    root.geometry("920x620+80+80")
    root.configure(bg="azure")
    app = VisitorManagementSystem(root, db_file_path)
    
    root.mainloop()
