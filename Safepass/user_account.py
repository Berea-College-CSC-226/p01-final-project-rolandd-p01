######################################################################
# Author: Dylan Roland
# Username: rolandd
#
# Assignment: P01
#
# Purpose: This module defines the UserAccount class, which handles
#          user authentication, password encryption, decryption,
#          and secure password management for the SafePass system.
#          It also ensures that all passwords are saved securely to
#          an encrypted JSON file for persistence.
#
######################################################################
# Acknowledgements:
#  Handled in safepass.py
#
####################################################################################


import os
import json
from cryptography.fernet import Fernet

class UserAccount:
    def __init__(self, username, password):
        """Initialize the user account with a username and master password."""
        self.username = username
        self.password = password
        self.key = self.load_encryption_key()  # Load a consistent encryption key
        self.cipher_suite = Fernet(self.key)
        self.passwords = self.load_passwords()  # Load passwords from JSON file

    @staticmethod
    def load_encryption_key():
        """Load the encryption key from file."""
        if not os.path.exists('data/encryption.key'):
            raise FileNotFoundError("Encryption key not found. Please ensure 'data/encryption.key' exists.")
        with open('data/encryption.key', 'rb') as key_file:
            return key_file.read()

    def load_passwords(self):
        """Load encrypted passwords from a JSON file."""
        passwords_file = f"data/{self.username}_passwords.json"
        if not os.path.exists(passwords_file):
            return {}

        with open(passwords_file, 'rb') as file:
            encrypted_data = file.read()

        try:
            decrypted_data = self.cipher_suite.decrypt(encrypted_data).decode()
            return json.loads(decrypted_data)
        except Exception as e:
            print(f"Error loading passwords for {self.username}: {e}")
            return {}

    def save_passwords_to_file(self):
        """Save encrypted passwords to a JSON file."""
        passwords_file = f"data/{self.username}_passwords.json"
        try:
            # Convert the passwords dictionary to JSON and encrypt it
            json_data = json.dumps(self.passwords)
            encrypted_data = self.cipher_suite.encrypt(json_data.encode())

            # Write the encrypted data to file
            with open(passwords_file, 'wb') as file:
                file.write(encrypted_data)
        except Exception as e:
            print(f"Error saving passwords for {self.username}: {e}")

    def encrypt_password(self, password):
        """Encrypt a plaintext password."""
        encrypted_password = self.cipher_suite.encrypt(password.encode())
        return encrypted_password.decode()  # Convert to string for storage

    def decrypt_password(self, encrypted_password):
        """Decrypt an encrypted password."""
        decrypted_password = self.cipher_suite.decrypt(encrypted_password.encode())
        return decrypted_password.decode()  # Convert back to string

    def save_password(self, site, password):
        """Save an encrypted password for a given site."""
        encrypted_password = self.encrypt_password(password)
        self.passwords[site] = encrypted_password
        self.save_passwords_to_file()
        return True

    def retrieve_password(self, site):
        """Retrieve and decrypt a password for a given site."""
        encrypted_password = self.passwords.get(site)
        if encrypted_password:
            return self.decrypt_password(encrypted_password)
        return None

    def remove_password(self, site):
        """Remove a saved password for a given site."""
        if site in self.passwords:
            del self.passwords[site]
            self.save_passwords_to_file()
            return True
        return False

    def list_sites(self):
        """List all the sites for which passwords are stored."""
        return list(self.passwords.keys())

    def export_passwords(self):
        """Export all passwords in a decrypted format (for debugging only)."""
        return {site: self.decrypt_password(enc_pass) for site, enc_pass in self.passwords.items()}

    def import_passwords(self, passwords):
        """Import a dictionary of plaintext passwords and store them encrypted."""
        for site, password in passwords.items():
            self.save_password(site, password)
