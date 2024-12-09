import os
import json
import bcrypt
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


def main():
    print("Welcome to SafePass - Your Secure Password Manager")
    print("-------------------------------------------------")

    # Initialize components
    user_data = load_user_data()
    account = None
    password_manager = PasswordManager()
    analyzer = PasswordStrengthAnalyzer()
    generator = AIPasswordGenerator()

    while True:
        print("\nMenu:")
        print("1. Create a New Account")
        print("2. Log In")
        print("3. Add a Password")
        print("4. Retrieve a Password")
        print("5. Analyze Password Strength")
        print("6. Generate a Secure Password")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            # Create a new user account
            username = input("Enter a new username: ")
            if username in user_data:
                print("Username already exists. Please choose a different username.")
                continue
            password = input("Enter a secure master password: ")
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            user_data[username] = {'password': hashed_password.decode()}
            save_user_data(user_data)
            print(f"Account for {username} created successfully!")

        elif choice == "2":
            # Log in to an existing account
            username = input("Enter your username: ")
            password = input("Enter your master password: ")
            if username in user_data:
                stored_hashed_password = user_data[username]['password'].encode()
                if bcrypt.checkpw(password.encode(), stored_hashed_password):
                    account = UserAccount(username, password)
                    print(f"Welcome back, {username}!")
                else:
                    print("Invalid password. Please try again.")
            else:
                print("Username does not exist. Please create an account first.")

        elif choice == "3":
            # Add a password to the manager
            if account:
                site = input("Enter the site name: ")
                password = input("Enter the password to save: ")
                password_manager.add_password(site, password)
                print(f"Password for {site} saved successfully!")
            else:
                print("Please log in first.")

        elif choice == "4":
            # Retrieve a password from the manager
            if account:
                site = input("Enter the site name to retrieve the password: ")
                password = password_manager.retrieve_password(site)
                if password:
                    print(f"Password for {site}: {password}")
                else:
                    print(f"No password found for {site}.")
            else:
                print("Please log in first.")

        elif choice == "5":
            # Analyze password strength
            password = input("Enter a password to analyze: ")
            result = analyzer.analyze_strength(password)
            print(f"Password Strength: {result['strength']}")
            if result["issues"]:
                print("Issues:")
                for issue in result["issues"]:
                    print(f"- {issue}")

        elif choice == "6":
            # Generate a secure password
            try:
                length = int(input("Enter desired password length (default is 12): "))
            except ValueError:
                length = 12
            include_special = input("Include special characters? (y/n): ").lower() == "y"
            generated_password = generator.generate_password(length=length, include_special=include_special)
            print(f"Generated Password: {generated_password}")

        elif choice == "7":
            # Exit the program
            print("Thank you for using SafePass. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
