# Générateur de Mot de Passe Sécurisé

Un générateur de mot de passe Python avec vérification de complexité et une section News sur les entreprises victimes de cyberattaques.

## Fonctionnalités

### 🔐 Génération de Mots de Passe
- Génération de mots de passe sécurisés et aléatoires
- Personnalisation de la longueur (défaut: 12 caractères)
- Options pour inclure/exclure:
  - Lettres majuscules
  - Lettres minuscules
  - Chiffres
  - Caractères spéciaux
- **Option pour exclure les caractères similaires** (0/O, 1/l/I, |)
- Génération de plusieurs mots de passe à la fois

### ✅ Vérification de Complexité
- Analyse de la force d'un mot de passe existant
- Vérification de:
  - Longueur minimale
  - Présence de majuscules
  - Présence de minuscules
  - Présence de chiffres
  - Présence de caractères spéciaux
- Score de complexité sur 7
- Recommandations pour améliorer la sécurité

### 📰 Section News
- Base de données des entreprises victimes de cyberattaques majeures
- Affichage de toutes les news
- Recherche par nom d'entreprise
- Affichage des N derniers incidents
- Informations détaillées:
  - Nom de l'entreprise
  - Date de l'incident
  - Nombre de comptes/personnes affectés
  - Type de données compromises

## Installation

```bash
# Cloner le dépôt
git clone https://github.com/Tom59sly/LesSupersIngenieursCitoyensEtClement.git
cd LesSupersIngenieursCitoyensEtClement

# Python 3.6+ est requis (aucune dépendance externe nécessaire)
```

## Utilisation

### Génération de Mots de Passe

```bash
# Générer un mot de passe par défaut (12 caractères)
python3 main.py

# Générer un mot de passe de 16 caractères
python3 main.py --length 16

# Exclure les caractères similaires (0/O, 1/l/I, |)
python3 main.py --exclude-similar

# Générer 5 mots de passe
python3 main.py --generate 5

# Générer un mot de passe sans caractères spéciaux
python3 main.py --no-special

# Générer un mot de passe de 20 caractères sans caractères similaires
python3 main.py --length 20 --exclude-similar
```

### Vérification de Complexité

```bash
# Vérifier la complexité d'un mot de passe
python3 main.py --check "MonMotDePasse123!"

# Exemples de sortie:
# - Longueur: X caractères
# - Présence de majuscules/minuscules/chiffres/spéciaux
# - Score: X/7
# - Recommandations d'amélioration
```

### Section News

```bash
# Afficher toutes les entreprises hackées
python3 main.py --news

# Afficher les 5 derniers incidents
python3 main.py --news --latest 5

# Rechercher des incidents pour une entreprise spécifique
python3 main.py --news --search Yahoo
python3 main.py --news --search Facebook
```

## Tests

```bash
# Lancer tous les tests
python3 -m unittest test_password_generator.py test_news.py -v

# Lancer uniquement les tests de génération
python3 -m unittest test_password_generator.py -v

# Lancer uniquement les tests de news
python3 -m unittest test_news.py -v
```

## Structure du Projet

```
.
├── main.py                      # Application principale (CLI)
├── password_generator.py        # Module de génération et vérification
├── news.py                      # Module de news sur les cyberattaques
├── test_password_generator.py   # Tests pour le générateur
├── test_news.py                 # Tests pour les news
└── README.md                    # Ce fichier
```

## Exemples

### Génération avec exclusion de caractères similaires

```bash
$ python3 main.py --exclude-similar --length 16

🔐 Génération de mot(s) de passe sécurisé(s)...

⚠️  Caractères similaires exclus (0/O, 1/l/I, |)

  ?GF-LW]a;5+GP-N8
  Score: 7/7 ✅ Fort

💡 Conseil: Ne réutilisez jamais le même mot de passe sur plusieurs sites!
```

### Vérification de complexité

```bash
$ python3 main.py --check "password"

🔍 Vérification de la complexité du mot de passe...

Longueur: 8 caractères
Minuscules: ✓
Majuscules: ✗
Chiffres: ✗
Caractères spéciaux: ✗

Score: 2/7

⚠️  Ce mot de passe est FAIBLE

Recommandations:
  • Ajouter des lettres majuscules
  • Ajouter des chiffres
  • Ajouter des caractères spéciaux
```

## Sécurité

### Bonnes Pratiques
- ✅ Utilisez des mots de passe de 12 caractères ou plus
- ✅ Incluez majuscules, minuscules, chiffres et caractères spéciaux
- ✅ N'utilisez jamais le même mot de passe sur plusieurs sites
- ✅ Utilisez un gestionnaire de mots de passe
- ✅ Activez l'authentification à deux facteurs (2FA)
- ✅ Changez vos mots de passe régulièrement

### Caractères Similaires
L'option `--exclude-similar` exclut les caractères qui peuvent être confondus:
- `0` (zéro) et `O` (lettre O majuscule)
- `1` (un) et `l` (lettre l minuscule) et `I` (lettre I majuscule)
- `|` (pipe) qui peut être confondu avec `l` ou `I`

Cette option est utile pour les mots de passe qui doivent être tapés manuellement.

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## Contributeurs

LesSupersIngenieursCitoyensEtClement