######################################################################
# Author: Dylan Roland
# Username: rolandd
#
# Assignment: P01
#
# Purpose: This module defines the AIPasswordGenerator class, which
#          generates secure, random passwords and validates them for
#          strength. The generator ensures passwords meet criteria for
#          uppercase, lowercase, digits, and special characters.
#
######################################################################
# Acknowledgements:
#   Handled in safepass.py
#
####################################################################################


import random
import string


class AIPasswordGenerator:
    def __init__(self):
        """Initialize the password generator with character pools."""
        self.letters = string.ascii_letters
        self.digits = string.digits
        self.special_chars = "!@#$%^&*"
        self.default_length = 12

    def generate_password(self, length=None, include_special=True):
        """
        Generate a random password.
        :param length: Desired length of the password (default is 12).
        :param include_special: Whether to include special characters.
        :return: A randomly generated password.
        """
        if length is None:
            length = self.default_length

        char_pool = self.letters + self.digits
        if include_special:
            char_pool += self.special_chars

        # Ensure at least one character from each category is included
        password = [
            random.choice(self.letters),
            random.choice(self.digits)
        ]
        if include_special:
            password.append(random.choice(self.special_chars))

        # Fill the rest of the password length
        password += random.choices(char_pool, k=length - len(password))

        # Shuffle to avoid predictable patterns
        random.shuffle(password)

        return ''.join(password)

    def validate_generated_password(self, password):
        """
        Validate the generated password for strength.
        :param password: The password to validate.
        :return: True if valid, False otherwise.
        """
        has_upper = any(char.isupper() for char in password)
        has_lower = any(char.islower() for char in password)
        has_digit = any(char.isdigit() for char in password)
        has_special = any(char in self.special_chars for char in password)

        return has_upper and has_lower and has_digit and has_special
