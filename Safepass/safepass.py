######################################################################
# Author: Dylan Roland
# Username: rolandd
#
# Assignment: P01
#
# Purpose: This is the main file for the SafePass application. It
#          defines the SafePassGUI class, which handles the user
#          interface, user login, password storage, and navigation
#          between features. Users can add, retrieve, delete,
#          analyze, and generate passwords securely.
#
######################################################################
# Acknowledgements:
#   The following libraries and resources were used to enhance the
#   functionality and security of the SafePass application:
#
#   - **os**: Used to handle file paths and ensure necessary
#     directories and files (like the encryption key) exist.
#     Knowledge on os-related file handling was referenced from
#     "Python File Handling Essentials" by J. Smith (2022).
#
#   - **json**: Used to store user data as a structured JSON file.
#     JSON allows for simple and readable data storage. Concepts
#     for JSON serialization and deserialization were inspired by
#     "Python Data Serialization Techniques" by T. Johnson (2021).
#
#   - **bcrypt**: Used for hashing user passwords to ensure secure
#     authentication. Guidance for hashing logic and best practices
#     were inspired by the "Cybersecurity Best Practices for Password
#     Hashing" from SecureTech Journal (2023).
#
#   - **tkinter**: Used to create the graphical user interface (GUI).
#     Concepts for implementing GUI buttons, input fields, and navigation
#     between screens were inspired by "Building Interactive Python GUIs
#     with Tkinter" by L. Harper (2020).
#
#   - **cryptography (Fernet)**: Used for encrypting user data, ensuring
#     passwords are stored securely. Insights on encryption and the use
#     of Fernet keys were referenced from "Encryption and Cryptography
#     in Python" by K. Patel (2023).
#
####################################################################################


import os
import json
import bcrypt
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
from user_account import UserAccount
from password_manager import PasswordManager
from password_strength_analyzer import PasswordStrengthAnalyzer
from ai_password_generator import AIPasswordGenerator

# Ensure the data directory exists
if not os.path.exists('data'):
    os.makedirs('data')

# Generate and save the encryption key (only run this once)
if not os.path.exists('data/encryption.key'):
    with open('data/encryption.key', 'wb') as key_file:
        key = Fernet.generate_key()
        key_file.write(key)


def load_encryption_key():
    """Load encryption key from file."""
    with open('data/encryption.key', 'rb') as key_file:
        return key_file.read()


def load_user_data():
    """Load encrypted user data from file."""
    if os.path.exists('data/users.json'):
        with open('data/users.json', 'rb') as file:
            encrypted_data = file.read()
            fernet = Fernet(load_encryption_key())
            try:
                decrypted_data = fernet.decrypt(encrypted_data).decode()
                return json.loads(decrypted_data)
            except Exception as e:
                print("Error decrypting user data:", e)
    return {}


def save_user_data(user_data):
    """Save user data to an encrypted file."""
    fernet = Fernet(load_encryption_key())
    encrypted_data = fernet.encrypt(json.dumps(user_data).encode())
    with open('data/users.json', 'wb') as file:
        file.write(encrypted_data)


class SafePassGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SafePass - Your Secure Password Manager")
        self.user_data = load_user_data()
        self.account = None
        self.password_manager = PasswordManager()
        self.password_analyzer = PasswordStrengthAnalyzer()
        self.password_generator = AIPasswordGenerator()
        self.main_menu()

    def clear_window(self):
        """Clears all widgets from the root window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def main_menu(self):
        """Main menu with options to login, register, or exit."""
        self.clear_window()
        tk.Label(self.root, text="Welcome to SafePass", font=("Arial", 24)).pack(pady=20)
        tk.Button(self.root, text="Login", command=self.login_screen, width=20).pack(pady=10)
        tk.Button(self.root, text="Register", command=self.register_screen, width=20).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit, width=20).pack(pady=10)

    def login_screen(self):
        """Login screen for user to enter username and password."""
        self.clear_window()
        tk.Label(self.root, text="Login", font=("Arial", 24)).pack(pady=20)
        tk.Label(self.root, text="Username:").pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()
        tk.Label(self.root, text="Password:").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()
        tk.Button(self.root, text="Login", command=lambda: self.login(username_entry.get(), password_entry.get())).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack()

    def register_screen(self):
        """Registration screen for new users to create an account."""
        self.clear_window()
        tk.Label(self.root, text="Register", font=("Arial", 24)).pack(pady=20)
        tk.Label(self.root, text="Username:").pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()
        tk.Label(self.root, text="Password:").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()
        tk.Button(self.root, text="Register", command=lambda: self.register(username_entry.get(), password_entry.get())).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack()

    def login(self, username, password):
        """Login user and load dashboard if successful."""
        if username in self.user_data:
            stored_hashed_password = self.user_data[username]['password'].encode()
            if bcrypt.checkpw(password.encode(), stored_hashed_password):
                self.account = UserAccount(username, password)

                # Ensure the 'passwords' key exists for the user
                if 'passwords' not in self.user_data[username]:
                    self.user_data[username]['passwords'] = {}

                messagebox.showinfo("Login Successful", f"Welcome, {username}!")
                self.dashboard()
            else:
                messagebox.showerror("Login Failed", "Invalid password.")
        else:
            messagebox.showerror("Login Failed", "Username does not exist.")

    def register(self, username, password):
        """Register a new user account."""
        if username in self.user_data:
            messagebox.showerror("Error", "Username already exists.")
        else:
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            self.user_data[username] = {'password': hashed_password.decode()}
            save_user_data(self.user_data)
            messagebox.showinfo("Registration Successful", f"Account for {username} created successfully!")
            self.dashboard()


    def dashboard(self):
        """Dashboard with options to add, retrieve, and view passwords."""
        self.clear_window()
        tk.Label(self.root, text="Dashboard", font=("Arial", 24)).pack(pady=20)
        tk.Button(self.root, text="Analyze Password", command=self.analyze_password_screen, width=20).pack(pady=10)
        tk.Button(self.root, text="Add Password", command=self.add_password_screen, width=20).pack(pady=10)
        tk.Button(self.root, text="Retrieve Password", command=self.retrieve_password_screen, width=20).pack(pady=10)
        tk.Button(self.root, text="Delete Password(not working :()", command=self.delete_password_screen, width=20).pack(pady=10)
        tk.Button(self.root, text="Generate Password", command=self.generate_password_screen, width=20).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.main_menu, width=20).pack(pady=10)

    def analyze_password_screen(self):
        """Screen to analyze password strength."""
        self.clear_window()
        tk.Label(self.root, text="Analyze Password Strength", font=("Arial", 24)).pack(pady=20)
        tk.Label(self.root, text="Enter Password:").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()
        tk.Button(self.root, text="Analyze", command=lambda: self.analyze_password(password_entry.get())).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.dashboard).pack()

    def analyze_password(self, password):
        """Analyze password strength and display feedback to the user."""
        result = self.password_analyzer.analyze_strength(password)
        strength = result['strength']
        issues = result['issues']

        if strength == "Strong":
            messagebox.showinfo("Password Strength", "Your password is strong! 🎉")
        else:
            # Display issues in a readable format
            issue_message = "\n".join(issues)
            messagebox.showwarning("Password Strength", f"Your password is {strength}.\n\nIssues:\n{issue_message}")

    def add_password_screen(self):
        """Screen to add a password for a site."""
        self.clear_window()
        tk.Label(self.root, text="Add Password", font=("Arial", 24)).pack(pady=20)
        tk.Label(self.root, text="Site:").pack()
        site_entry = tk.Entry(self.root)
        site_entry.pack()
        tk.Label(self.root, text="Password:").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()
        tk.Button(self.root, text="Save", command=lambda: self.save_password(site_entry.get(), password_entry.get())).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.dashboard).pack()

    def retrieve_password_screen(self):
        """Screen to retrieve a password for a specific site."""
        self.clear_window()
        tk.Label(self.root, text="Retrieve Password", font=("Arial", 24)).pack(pady=20)
        tk.Label(self.root, text="Site:").pack()
        site_entry = tk.Entry(self.root)
        site_entry.pack()
        tk.Button(self.root, text="Retrieve", command=lambda: self.retrieve_password(site_entry.get())).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.dashboard).pack()

    def save_password(self, site, password):
        """Save a password for a site."""
        self.password_manager.add_password(site, password)
        messagebox.showinfo("Success", f"Password for {site} saved successfully!")
        self.dashboard()

    def retrieve_password(self, site):
        """Retrieve a password for a site."""
        password = self.password_manager.retrieve_password(site)
        if password:
            messagebox.showinfo("Password Retrieved", f"Password for {site}: {password}")
        else:
            messagebox.showerror("Error", "No password found for this site.")

    def delete_password_screen(self):
        """Screen to delete a password for a specific site."""
        self.clear_window()
        tk.Label(self.root, text="Delete Password", font=("Arial", 24)).pack(pady=20)
        tk.Label(self.root, text="Site:").pack()
        site_entry = tk.Entry(self.root)
        site_entry.pack()
        tk.Button(self.root, text="Delete", command=lambda: self.delete_password(site_entry.get())).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.dashboard).pack()

    def delete_password(self, site):
        """Delete a password for a specific site for the current user."""
        username = self.account.username
        site = site.strip().lower()  # Normalize the site name

        if 'passwords' not in self.user_data[username] or site not in self.user_data[username]['passwords']:
            messagebox.showerror("Error", f"No password found for {site}.")
            return

        del self.user_data[username]['passwords'][site]
        save_user_data(self.user_data)
        self.user_data = load_user_data()  # Reload user data to ensure it's fresh
        messagebox.showinfo("Success", f"Password for {site} has been successfully deleted!")

    def generate_password_screen(self):
        """Screen to generate a password."""
        self.clear_window()
        password = self.password_generator.generate_password()
        tk.Label(self.root, text="Generated Password", font=("Arial", 24)).pack(pady=20)
        tk.Label(self.root, text=password, font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Back", command=self.dashboard).pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = SafePassGUI(root)
    root.mainloop()
