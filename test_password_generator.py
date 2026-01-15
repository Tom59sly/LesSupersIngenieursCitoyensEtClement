"""
Tests pour le générateur de mot de passe.
"""
import unittest
from password_generator import PasswordGenerator


class TestPasswordGenerator(unittest.TestCase):
    """Tests pour la classe PasswordGenerator."""
    
    def test_default_generation(self):
        """Test la génération par défaut."""
        generator = PasswordGenerator()
        password = generator.generate()
        self.assertEqual(len(password), 12)
    
    def test_custom_length(self):
        """Test la génération avec longueur personnalisée."""
        for length in [8, 16, 20, 32]:
            generator = PasswordGenerator(length=length)
            password = generator.generate()
            self.assertEqual(len(password), length)
    
    def test_exclude_similar_characters(self):
        """Test l'exclusion des caractères similaires."""
        generator = PasswordGenerator(length=100, exclude_similar=True)
        password = generator.generate()
        
        # Vérifier qu'aucun caractère similaire n'est présent
        similar_chars = 'iloIO01|'
        for char in similar_chars:
            self.assertNotIn(char, password, 
                           f"Le caractère similaire '{char}' ne devrait pas être présent")
    
    def test_only_lowercase(self):
        """Test génération avec uniquement des minuscules."""
        generator = PasswordGenerator(
            use_uppercase=False,
            use_digits=False,
            use_special=False
        )
        password = generator.generate()
        self.assertTrue(password.islower())
    
    def test_no_character_types_raises_error(self):
        """Test qu'une erreur est levée si aucun type de caractère n'est activé."""
        generator = PasswordGenerator(
            use_uppercase=False,
            use_lowercase=False,
            use_digits=False,
            use_special=False
        )
        with self.assertRaises(ValueError):
            generator.generate()
    
    def test_length_too_short_for_all_types(self):
        """Test qu'une erreur est levée si la longueur est trop courte."""
        # Avec 4 types de caractères, la longueur minimale est 4
        generator = PasswordGenerator(length=3)
        with self.assertRaises(ValueError) as context:
            generator.generate()
        self.assertIn("au moins 4", str(context.exception))
    
    def test_all_character_types_present(self):
        """Test que tous les types de caractères sont présents."""
        generator = PasswordGenerator(length=20)
        # Générer plusieurs fois pour s'assurer que la probabilité est bonne
        for _ in range(10):
            password = generator.generate()
            complexity = PasswordGenerator.check_complexity(password)
            
            self.assertTrue(complexity['has_lowercase'], 
                          f"Minuscules manquantes dans: {password}")
            self.assertTrue(complexity['has_uppercase'],
                          f"Majuscules manquantes dans: {password}")
            self.assertTrue(complexity['has_digit'],
                          f"Chiffres manquants dans: {password}")
            self.assertTrue(complexity['has_special'],
                          f"Caractères spéciaux manquants dans: {password}")


class TestPasswordComplexity(unittest.TestCase):
    """Tests pour la vérification de complexité."""
    
    def test_strong_password(self):
        """Test un mot de passe fort."""
        result = PasswordGenerator.check_complexity("MyStr0ng!P@ssw0rd")
        self.assertTrue(result['is_strong'])
        self.assertTrue(result['has_lowercase'])
        self.assertTrue(result['has_uppercase'])
        self.assertTrue(result['has_digit'])
        self.assertTrue(result['has_special'])
    
    def test_weak_password_too_short(self):
        """Test un mot de passe trop court."""
        result = PasswordGenerator.check_complexity("Pass1!")
        self.assertFalse(result['is_strong'])
        self.assertLess(result['length'], 8)
    
    def test_weak_password_no_uppercase(self):
        """Test un mot de passe sans majuscule."""
        result = PasswordGenerator.check_complexity("password123!")
        self.assertFalse(result['is_strong'])
        self.assertFalse(result['has_uppercase'])
    
    def test_weak_password_no_digits(self):
        """Test un mot de passe sans chiffres."""
        result = PasswordGenerator.check_complexity("Password!!")
        self.assertFalse(result['is_strong'])
        self.assertFalse(result['has_digit'])
    
    def test_weak_password_no_special(self):
        """Test un mot de passe sans caractères spéciaux."""
        result = PasswordGenerator.check_complexity("Password123")
        self.assertFalse(result['has_special'])
    
    def test_complexity_score(self):
        """Test le calcul du score de complexité."""
        # Mot de passe très simple
        result = PasswordGenerator.check_complexity("pass")
        self.assertLess(result['score'], 3)
        
        # Mot de passe moyen
        result = PasswordGenerator.check_complexity("Password")
        self.assertGreater(result['score'], 2)
        self.assertLess(result['score'], 5)
        
        # Mot de passe fort
        result = PasswordGenerator.check_complexity("MyStr0ng!P@ssw0rd123")
        self.assertGreater(result['score'], 5)
    
    def test_feedback_messages(self):
        """Test les messages de feedback."""
        result = PasswordGenerator.check_complexity("pass")
        self.assertGreater(len(result['feedback']), 0)
        
        result = PasswordGenerator.check_complexity("MyStr0ng!P@ssw0rd")
        self.assertIn("Mot de passe fort ✓", result['feedback'])


if __name__ == '__main__':
    unittest.main()
