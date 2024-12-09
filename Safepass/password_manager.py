import os
from cryptography.fernet import Fernet

class PasswordManager:
    def __init__(self):
        """Initialize the password manager with dictionaries to store passwords and categories."""
        self.passwords = {}  # Dictionary to store site-password pairs (encrypted)
        self.categories = {}  # Dictionary to store categories for sites

    @staticmethod
    def load_encryption_key():
        """Load the encryption key from file."""
        if not os.path.exists('data/encryption.key'):
            raise FileNotFoundError("Encryption key not found. Please ensure 'data/encryption.key' exists.")
        with open('data/encryption.key', 'rb') as key_file:
            return key_file.read()

    @staticmethod
    def encrypt_password(plaintext_password):
        """Encrypt a plaintext password using AES encryption (Fernet)."""
        key = PasswordManager.load_encryption_key()
        fernet = Fernet(key)
        encrypted_password = fernet.encrypt(plaintext_password.encode())
        return encrypted_password.decode()  # Convert to string for storage

    @staticmethod
    def decrypt_password(encrypted_password):
        """Decrypt an encrypted password back into plaintext."""
        key = PasswordManager.load_encryption_key()
        fernet = Fernet(key)
        decrypted_password = fernet.decrypt(encrypted_password.encode())
        return decrypted_password.decode()  # Convert back to string

    def add_password(self, site, password, category=None):
        """Add a password for a specific site, encrypt it, and store it."""
        encrypted_password = self.encrypt_password(password)
        self.passwords[site] = encrypted_password
        if category:
            self.categories[site] = category

    def remove_password(self, site):
        """Remove a password for a specific site."""
        if site in self.passwords:
            del self.passwords[site]
            if site in self.categories:
                del self.categories[site]
            return True
        return False

    def retrieve_password(self, site):
        """Retrieve and decrypt the password for a specific site."""
        if site in self.passwords:
            encrypted_password = self.passwords[site]
            decrypted_password = self.decrypt_password(encrypted_password)
            return decrypted_password
        return None

    def categorize_password(self, site, category):
        """Assign a category to a specific site."""
        if site in self.passwords:
            self.categories[site] = category
            return True
        return False

    def get_passwords_by_category(self, category):
        """Retrieve all sites in a specific category."""
        return [site for site, cat in self.categories.items() if cat == category]

    def list_all_passwords(self):
        """List all stored passwords (for debugging or testing purposes)."""
        # Decrypt all stored passwords for display purposes
        return {site: self.decrypt_password(enc_pass) for site, enc_pass in self.passwords.items()}
