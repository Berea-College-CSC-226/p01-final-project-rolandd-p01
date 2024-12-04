class PasswordManager:
    def __init__(self):
        """Initialize the password manager with an empty dictionary to store passwords."""
        self.passwords = {}  # Dictionary to store site-password pairs
        self.categories = {}  # Dictionary to store categories for sites

    def add_password(self, site, password, category=None):
        """Add a password for a specific site."""
        self.passwords[site] = password
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
        """Retrieve the password for a specific site."""
        return self.passwords.get(site, None)

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
        return self.passwords
