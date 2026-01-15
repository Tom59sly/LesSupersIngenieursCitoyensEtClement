#!/usr/bin/env python3
"""
Application principale pour le générateur de mot de passe sécurisé.
"""
import argparse
import sys
from password_generator import PasswordGenerator
from news import HackNewsDatabase


def main():
    """Point d'entrée principal de l'application."""
    parser = argparse.ArgumentParser(
        description='Générateur de mot de passe sécurisé avec vérification de complexité',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  %(prog)s                              # Génère un mot de passe par défaut
  %(prog)s --length 16                  # Génère un mot de passe de 16 caractères
  %(prog)s --exclude-similar            # Exclut les caractères similaires (i/l/o, I/O, 0/1, |)
  %(prog)s --check "MonMotDePasse123!"  # Vérifie la complexité d'un mot de passe
  %(prog)s --news                       # Affiche les entreprises hackées
  %(prog)s --news --search Yahoo        # Recherche des infos sur Yahoo
        """
    )
    
    # Options de génération
    parser.add_argument('-l', '--length', type=int, default=12,
                       help='Longueur du mot de passe (défaut: 12)')
    parser.add_argument('--no-uppercase', action='store_true',
                       help='Ne pas inclure de majuscules')
    parser.add_argument('--no-lowercase', action='store_true',
                       help='Ne pas inclure de minuscules')
    parser.add_argument('--no-digits', action='store_true',
                       help='Ne pas inclure de chiffres')
    parser.add_argument('--no-special', action='store_true',
                       help='Ne pas inclure de caractères spéciaux')
    parser.add_argument('--exclude-similar', action='store_true',
                       help='Exclure les caractères similaires (i/l/o, I/O, 0/1, |)')
    
    # Options de vérification
    parser.add_argument('-c', '--check', type=str,
                       help='Vérifier la complexité d\'un mot de passe existant')
    
    # Options news
    parser.add_argument('-n', '--news', action='store_true',
                       help='Afficher les news sur les entreprises hackées')
    parser.add_argument('--search', type=str,
                       help='Rechercher des incidents pour une entreprise spécifique')
    parser.add_argument('--latest', type=int,
                       help='Afficher les N derniers incidents')
    
    # Options générales
    parser.add_argument('-g', '--generate', type=int, default=1,
                       help='Nombre de mots de passe à générer (défaut: 1)')
    
    args = parser.parse_args()
    
    # Affichage des news
    if args.news:
        news_db = HackNewsDatabase()
        
        if args.search:
            incidents = news_db.search_by_company(args.search)
            if incidents:
                print(f"\n🔍 Incidents trouvés pour '{args.search}':\n")
                for incident in incidents:
                    print(news_db.format_news(incident))
            else:
                print(f"\nAucun incident trouvé pour '{args.search}'")
        elif args.latest:
            print(f"\n📰 {args.latest} derniers incidents:\n")
            for incident in news_db.get_latest_news(args.latest):
                print(news_db.format_news(incident))
        else:
            news_db.display_all_news()
        
        return 0
    
    # Vérification de complexité
    if args.check:
        print("\n🔍 Vérification de la complexité du mot de passe...\n")
        result = PasswordGenerator.check_complexity(args.check)
        
        print(f"Longueur: {result['length']} caractères")
        print(f"Minuscules: {'✓' if result['has_lowercase'] else '✗'}")
        print(f"Majuscules: {'✓' if result['has_uppercase'] else '✗'}")
        print(f"Chiffres: {'✓' if result['has_digit'] else '✗'}")
        print(f"Caractères spéciaux: {'✓' if result['has_special'] else '✗'}")
        print(f"\nScore: {result['score']}/7")
        
        if result['is_strong']:
            print("\n✅ Ce mot de passe est FORT")
        else:
            print("\n⚠️  Ce mot de passe est FAIBLE")
            print("\nRecommandations:")
            for feedback in result['feedback']:
                print(f"  • {feedback}")
        
        return 0
    
    # Génération de mot de passe
    try:
        generator = PasswordGenerator(
            length=args.length,
            use_uppercase=not args.no_uppercase,
            use_lowercase=not args.no_lowercase,
            use_digits=not args.no_digits,
            use_special=not args.no_special,
            exclude_similar=args.exclude_similar
        )
        
        print("\n🔐 Génération de mot(s) de passe sécurisé(s)...\n")
        
        if args.exclude_similar:
            print("⚠️  Caractères similaires exclus (i/l/o, I/O, 0/1, |)\n")
        
        for i in range(args.generate):
            password = generator.generate()
            complexity = PasswordGenerator.check_complexity(password)
            
            if args.generate > 1:
                print(f"Mot de passe #{i+1}:")
            
            print(f"  {password}")
            print(f"  Score: {complexity['score']}/7 {'✅ Fort' if complexity['is_strong'] else '⚠️  Faible'}")
            
            if args.generate > 1:
                print()
        
        print("\n💡 Conseil: Ne réutilisez jamais le même mot de passe sur plusieurs sites!")
        print("💡 Utilisez un gestionnaire de mots de passe pour les stocker en sécurité.")
        
    except ValueError as e:
        print(f"Erreur: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
