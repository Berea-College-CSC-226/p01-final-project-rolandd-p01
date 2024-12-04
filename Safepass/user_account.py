from cryptography.fernet import Fernet

class UserAccount:
    def __init__(self, username, password):
        """Initialize the user account with a username and encryption key."""
        self.username = username
        self.password = password
        self.key = Fernet.generate_key()  # Generate a unique key for encryption
        self.cipher_suite = Fernet(self.key)
        self.passwords = {}  # Dictionary to store encrypted passwords for sites

    def encrypt_password(self, password):
        """Encrypt a plaintext password."""
        return self.cipher_suite.encrypt(password.encode())

    def decrypt_password(self, encrypted_password):
        """Decrypt an encrypted password."""
        return self.cipher_suite.decrypt(encrypted_password).decode()

    def save_password(self, site, password):
        """Save an encrypted password for a given site."""
        encrypted_password = self.encrypt_password(password)
        self.passwords[site] = encrypted_password
        return True

    def retrieve_password(self, site):
        """Retrieve and decrypt a password for a given site."""
        encrypted_password = self.passwords.get(site)
        if encrypted_password:
            return self.decrypt_password(encrypted_password)
        return None
