from user_account import UserAccount
from password_manager import PasswordManager
from password_strength_analyzer import PasswordStrengthAnalyzer
from ai_password_generator import AIPasswordGenerator


def main():
    print("Welcome to SafePass - Your Secure Password Manager")
    print("-------------------------------------------------")

    # Initialize components
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
            password = input("Enter a secure master password: ")
            account = UserAccount(username, password)
            print(f"Account for {username} created successfully!")

        elif choice == "2":
            # Log in to an existing account (Placeholder logic)
            username = input("Enter your username: ")
            password = input("Enter your master password: ")
            if account and account.username == username and account.password == password:
                print(f"Welcome back, {username}!")
            else:
                print("Invalid username or password. Try again.")

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
            length = int(input("Enter desired password length (default is 12): "))
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
