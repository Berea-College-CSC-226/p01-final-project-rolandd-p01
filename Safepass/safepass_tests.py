import unittest
from user_account import UserAccount
from password_manager import PasswordManager
from password_strength_analyzer import PasswordStrengthAnalyzer
from ai_password_generator import AIPasswordGenerator


# UserAccount Tests
class TestUserAccount(unittest.TestCase):
    def setUp(self):
        self.account = UserAccount("testuser", "testpassword")

    def test_encrypt_decrypt_password(self):
        encrypted = self.account.encrypt_password("mypassword")
        decrypted = self.account.decrypt_password(encrypted)
        self.assertEqual(decrypted, "mypassword")

    def test_save_password(self):
        self.assertTrue(self.account.save_password("example.com", "securePass123"))
        self.assertIn("example.com", self.account.passwords)

    def test_retrieve_password(self):
        self.account.save_password("example.com", "securePass123")
        retrieved_password = self.account.retrieve_password("example.com")
        self.assertEqual(retrieved_password, "securePass123")

    def test_retrieve_nonexistent_password(self):
        self.assertIsNone(self.account.retrieve_password("nonexistent.com"))


# PasswordManager Tests
class TestPasswordManager(unittest.TestCase):
    def setUp(self):
        self.manager = PasswordManager()

    def test_add_password(self):
        self.manager.add_password("example.com", "password123", "Work")
        self.assertEqual(self.manager.retrieve_password("example.com"), "password123")

    def test_remove_password(self):
        self.manager.add_password("example.com", "password123")
        self.assertTrue(self.manager.remove_password("example.com"))
        self.assertIsNone(self.manager.retrieve_password("example.com"))

    def test_retrieve_password(self):
        self.manager.add_password("example.com", "password123")
        self.assertEqual(self.manager.retrieve_password("example.com"), "password123")
        self.assertIsNone(self.manager.retrieve_password("nonexistent.com"))

    def test_categorize_password(self):
        self.manager.add_password("example.com", "password123")
        self.assertTrue(self.manager.categorize_password("example.com", "Work"))
        self.assertEqual(self.manager.get_passwords_by_category("Work"), ["example.com"])

    def test_get_passwords_by_category(self):
        self.manager.add_password("example.com", "password123", "Work")
        self.manager.add_password("personal.com", "mypassword", "Personal")
        self.assertEqual(self.manager.get_passwords_by_category("Work"), ["example.com"])
        self.assertEqual(self.manager.get_passwords_by_category("Personal"), ["personal.com"])
        self.assertEqual(self.manager.get_passwords_by_category("Nonexistent"), [])

    def test_list_all_passwords(self):
        self.manager.add_password("example.com", "password123")
        self.manager.add_password("personal.com", "mypassword")
        self.assertEqual(len(self.manager.list_all_passwords()), 2)


# PasswordStrengthAnalyzer Tests
class TestPasswordStrengthAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = PasswordStrengthAnalyzer()

    def test_analyze_strength_strong_password(self):
        result = self.analyzer.analyze_strength("Str0ng!Pass")
        self.assertEqual(result["strength"], "Strong")
        self.assertEqual(result["issues"], [])

    def test_analyze_strength_weak_password(self):
        result = self.analyzer.analyze_strength("weakpass")
        self.assertEqual(result["strength"], "Weak")
        self.assertIn("Password must contain at least one uppercase letter.", result["issues"])
        self.assertIn("Password must contain at least one digit.", result["issues"])
        self.assertIn("Password must contain at least one special character (!@#$%^&*).", result["issues"])

    def test_suggest_improvement(self):
        suggestions = self.analyzer.suggest_improvement("weakpass")
        self.assertIn("Password must contain at least one uppercase letter.", suggestions)
        self.assertIn("Password must contain at least one digit.", suggestions)


# AIPasswordGenerator Tests
class TestAIPasswordGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = AIPasswordGenerator()

    def test_generate_password(self):
        password = self.generator.generate_password()
        self.assertEqual(len(password), 12)  # Default length
        self.assertTrue(self.generator.validate_generated_password(password))

    def test_generate_password_custom_length(self):
        password = self.generator.generate_password(length=16)
        self.assertEqual(len(password), 16)

    def test_generate_password_no_special(self):
        password = self.generator.generate_password(include_special=False)
        self.assertTrue(all(char.isalnum() for char in password))

    def test_validate_generated_password(self):
        strong_password = "Aa1@Strong"
        weak_password = "weakpassword"
        self.assertTrue(self.generator.validate_generated_password(strong_password))
        self.assertFalse(self.generator.validate_generated_password(weak_password))


if __name__ == "__main__":
    unittest.main()
