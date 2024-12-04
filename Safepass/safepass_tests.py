import unittest
from user_account import UserAccount
from password_manager import PasswordManager
from password_strength_analyzer import PasswordStrengthAnalyzer
from ai_password_generator import AIPasswordGenerator

    class TestUserAccount(unittest.TestCase):

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

    if __name__ == "__main__":
        unittest.main()

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

    if __name__ == "__main__":
        unittest.main()


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
