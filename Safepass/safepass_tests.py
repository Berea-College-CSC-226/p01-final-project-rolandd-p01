import unittest
from user_account import UserAccount
from password_manager import PasswordManager
from password_strength_analyzer import PasswordStrengthAnalyzer
from ai_password_generator import AIPasswordGenerator

class TestUserAccount(unittest.TestCase):
    def test_encrypt_password(self):
        account = UserAccount("testuser", "testpassword")
        self.assertIsNone(account.encrypt_password("testpassword"))

    def test_decrypt_password(self):
        account = UserAccount("testuser", "testpassword")
        self.assertIsNone(account.decrypt_password("encryptedpassword"))

class TestPasswordManager(unittest.TestCase):
    def test_add_password(self):
        manager = PasswordManager()
        self.assertIsNone(manager.add_password("testsite", "testpassword"))

class TestPasswordStrengthAnalyzer(unittest.TestCase):
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

    if __name__ == "__main__":
        unittest.main()


class TestAIPasswordGenerator(unittest.TestCase):
    def test_generate_password(self):
        generator = AIPasswordGenerator()
        self.assertIsNone(generator.generate_password())

if __name__ == "__main__":
    unittest.main()
