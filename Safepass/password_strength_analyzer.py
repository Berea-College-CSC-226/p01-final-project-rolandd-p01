######################################################################
# Author: Dylan Roland
# Username: rolandd
#
# Assignment: P01
#
# Purpose: This module defines the PasswordStrengthAnalyzer class,
#          which analyzes and evaluates the strength of user passwords.
#          It provides feedback on improvements to ensure passwords
#          meet security standards for length, character variety,
#          and complexity.
#
######################################################################
# Acknowledgements:
#   Handled in safepass.py
#
####################################################################################


class PasswordStrengthAnalyzer:
    def __init__(self):
        self.min_length = 8  # Minimum password length
        self.rules = {
            "uppercase": "Password must contain at least one uppercase letter.",
            "lowercase": "Password must contain at least one lowercase letter.",
            "digit": "Password must contain at least one digit.",
            "special": "Password must contain at least one special character (!@#$%^&*)."
        }
        self.special_characters = "!@#$%^&*"

    def analyze_strength(self, password):
        """Analyzes the strength of a given password."""
        issues = []
        if len(password) < self.min_length:
            issues.append(f"Password must be at least {self.min_length} characters long.")
        if not any(char.isupper() for char in password):
            issues.append(self.rules["uppercase"])
        if not any(char.islower() for char in password):
            issues.append(self.rules["lowercase"])
        if not any(char.isdigit() for char in password):
            issues.append(self.rules["digit"])
        if not any(char in self.special_characters for char in password):
            issues.append(self.rules["special"])

        if issues:
            return {"strength": "Weak", "issues": issues}
        return {"strength": "Strong", "issues": []}

    def suggest_improvement(self, password):
        """Provides suggestions for improving the strength of a given password."""
        analysis = self.analyze_strength(password)
        if analysis["strength"] == "Strong":
            return "Your password is strong. No changes needed."
        return "Suggestions to improve your password:\n" + "\n".join(analysis["issues"])
