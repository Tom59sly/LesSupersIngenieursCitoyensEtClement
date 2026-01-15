"""
Générateur de mot de passe avec vérification de complexité.
"""
import random
import string
import re


class PasswordGenerator:
    """Générateur de mots de passe sécurisés avec vérification de complexité."""
    
    # Caractères similaires qui peuvent être confondus
    SIMILAR_CHARS = {
        'lowercase': 'ilo',
        'uppercase': 'IO',
        'digits': '01',
        'special': '|'
    }
    
    def __init__(self, length=12, use_uppercase=True, use_lowercase=True, 
                 use_digits=True, use_special=True, exclude_similar=False):
        """
        Initialise le générateur de mot de passe.
        
        Args:
            length: Longueur du mot de passe (défaut: 12)
            use_uppercase: Inclure des majuscules (défaut: True)
            use_lowercase: Inclure des minuscules (défaut: True)
            use_digits: Inclure des chiffres (défaut: True)
            use_special: Inclure des caractères spéciaux (défaut: True)
            exclude_similar: Exclure les caractères similaires (défaut: False)
        """
        self.length = length
        self.use_uppercase = use_uppercase
        self.use_lowercase = use_lowercase
        self.use_digits = use_digits
        self.use_special = use_special
        self.exclude_similar = exclude_similar
        
    def _get_character_sets(self):
        """Retourne les ensembles de caractères à utiliser."""
        char_sets = []
        
        if self.use_lowercase:
            chars = string.ascii_lowercase
            if self.exclude_similar:
                chars = ''.join(c for c in chars if c not in self.SIMILAR_CHARS['lowercase'])
            char_sets.append(chars)
            
        if self.use_uppercase:
            chars = string.ascii_uppercase
            if self.exclude_similar:
                chars = ''.join(c for c in chars if c not in self.SIMILAR_CHARS['uppercase'])
            char_sets.append(chars)
            
        if self.use_digits:
            chars = string.digits
            if self.exclude_similar:
                chars = ''.join(c for c in chars if c not in self.SIMILAR_CHARS['digits'])
            char_sets.append(chars)
            
        if self.use_special:
            chars = "!@#$%^&*()-_=+[]{}\\;:'\",.<>?/"
            if self.exclude_similar:
                chars = ''.join(c for c in chars if c not in self.SIMILAR_CHARS['special'])
            char_sets.append(chars)
            
        return char_sets
    
    def generate(self):
        """
        Génère un mot de passe aléatoire.
        
        Returns:
            str: Le mot de passe généré
        """
        char_sets = self._get_character_sets()
        
        if not char_sets:
            raise ValueError("Au moins un type de caractère doit être activé")
        
        if self.length < len(char_sets):
            raise ValueError(
                f"La longueur doit être au moins {len(char_sets)} pour inclure "
                f"tous les types de caractères actifs"
            )
        
        # S'assurer qu'au moins un caractère de chaque ensemble est inclus
        password = []
        for char_set in char_sets:
            password.append(random.choice(char_set))
        
        # Remplir le reste avec des caractères aléatoires
        all_chars = ''.join(char_sets)
        while len(password) < self.length:
            password.append(random.choice(all_chars))
        
        # Mélanger le mot de passe
        random.shuffle(password)
        
        return ''.join(password)
    
    @staticmethod
    def check_complexity(password):
        """
        Vérifie la complexité d'un mot de passe.
        
        Args:
            password: Le mot de passe à vérifier
            
        Returns:
            dict: Dictionnaire avec les résultats de la vérification
        """
        result = {
            'length': len(password),
            'has_lowercase': bool(re.search(r'[a-z]', password)),
            'has_uppercase': bool(re.search(r'[A-Z]', password)),
            'has_digit': bool(re.search(r'\d', password)),
            'has_special': bool(re.search(r'[^a-zA-Z0-9]', password)),
            'is_strong': False,
            'score': 0,
            'feedback': []
        }
        
        # Calculer le score
        if result['length'] >= 8:
            result['score'] += 1
        if result['length'] >= 12:
            result['score'] += 1
        if result['length'] >= 16:
            result['score'] += 1
            
        if result['has_lowercase']:
            result['score'] += 1
        if result['has_uppercase']:
            result['score'] += 1
        if result['has_digit']:
            result['score'] += 1
        if result['has_special']:
            result['score'] += 1
        
        # Générer les feedbacks
        if result['length'] < 8:
            result['feedback'].append("Le mot de passe est trop court (minimum 8 caractères)")
        if not result['has_lowercase']:
            result['feedback'].append("Ajouter des lettres minuscules")
        if not result['has_uppercase']:
            result['feedback'].append("Ajouter des lettres majuscules")
        if not result['has_digit']:
            result['feedback'].append("Ajouter des chiffres")
        if not result['has_special']:
            result['feedback'].append("Ajouter des caractères spéciaux")
        
        # Déterminer si le mot de passe est fort
        result['is_strong'] = (result['score'] >= 5 and 
                              result['length'] >= 8 and
                              result['has_lowercase'] and
                              result['has_uppercase'] and
                              result['has_digit'])
        
        if result['is_strong']:
            result['feedback'].append("Mot de passe fort ✓")
        
        return result
