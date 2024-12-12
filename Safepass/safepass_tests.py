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
        """Test that encrypting and decrypting a password returns the original password."""
        encrypted = self.account.encrypt_password("mypassword")
        decrypted = self.account.decrypt_password(encrypted)
        self.assertEqual(decrypted, "mypassword")

    def test_encrypt_password_is_not_plaintext(self):
        """Test that encrypted passwords are different from the original."""
        plaintext_password = "mypassword"
        encrypted_password = self.account.encrypt_password(plaintext_password)
        self.assertNotEqual(encrypted_password, plaintext_password)

    def test_save_password(self):
        """Test that passwords are saved properly and encrypted."""
        self.assertTrue(self.account.save_password("example.com", "securePass123"))
        self.assertIn("example.com", self.account.passwords)

    def test_retrieve_password(self):
        """Test that passwords can be retrieved correctly."""
        self.account.save_password("example.com", "securePass123")
        retrieved_password = self.account.retrieve_password("example.com")
        self.assertEqual(retrieved_password, "securePass123")

    def test_retrieve_nonexistent_password(self):
        """Test that retrieving a non-existent password returns None."""
        self.assertIsNone(self.account.retrieve_password("nonexistent.com"))

    def test_remove_password(self):
        """Test that passwords can be removed."""
        self.account.save_password("example.com", "securePass123")
        self.assertTrue(self.account.remove_password("example.com"))
        self.assertIsNone(self.account.retrieve_password("example.com"))

    def test_list_sites(self):
        """Test that list_sites correctly lists all sites with stored passwords."""
        self.account.save_password("example.com", "securePass123")
        self.account.save_password("another.com", "Password456")
        self.assertEqual(set(self.account.list_sites()), {"example.com", "another.com"})

    def test_wrong_key_decryption(self):
        """Test that decryption with a different key fails."""
        encrypted = self.account.encrypt_password("mypassword")
        original_load_key = UserAccount.load_encryption_key
        UserAccount.load_encryption_key = lambda: b'wrongkeywrongkeywrongkeywronk'
        with self.assertRaises(Exception):
            self.account.decrypt_password(encrypted)
        UserAccount.load_encryption_key = original_load_key


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
        self.assertEqual(len(password), 12)
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

    def test_generated_password_meets_strength_requirements(self):
        password = self.generator.generate_password()
        analyzer = PasswordStrengthAnalyzer()
        result = analyzer.analyze_strength(password)
        self.assertEqual(result["strength"], "Strong", "Generated password does not meet strength requirements")


# Run all tests
if __name__ == "__main__":
    unittest.main()
