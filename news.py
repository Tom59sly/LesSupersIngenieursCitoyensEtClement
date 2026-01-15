"""
Module de news sur les entreprises victimes de hacks.
"""
from datetime import datetime


class HackNewsDatabase:
    """Base de données des entreprises qui se sont fait hacker."""
    
    # Base de données des incidents de sécurité connus
    HACKED_COMPANIES = [
        {
            'company': 'Yahoo',
            'date': '2013-2014',
            'description': '3 milliards de comptes compromis',
            'impact': 'Emails, mots de passe, questions de sécurité'
        },
        {
            'company': 'Equifax',
            'date': '2017',
            'description': '147 millions de personnes affectées',
            'impact': 'Numéros de sécurité sociale, dates de naissance, adresses'
        },
        {
            'company': 'Facebook',
            'date': '2019',
            'description': '540 millions de données exposées',
            'impact': 'Commentaires, likes, identifiants utilisateurs'
        },
        {
            'company': 'Marriott',
            'date': '2018',
            'description': '500 millions de clients affectés',
            'impact': 'Informations de réservation, passeports, cartes de crédit'
        },
        {
            'company': 'LinkedIn',
            'date': '2021',
            'description': '700 millions de profils exposés',
            'impact': 'Emails, numéros de téléphone, informations professionnelles'
        },
        {
            'company': 'Adobe',
            'date': '2013',
            'description': '153 millions de comptes compromis',
            'impact': 'Identifiants, mots de passe, informations de carte bancaire'
        },
        {
            'company': 'Uber',
            'date': '2016',
            'description': '57 millions de comptes affectés',
            'impact': 'Noms, emails, numéros de téléphone de conducteurs et passagers'
        },
        {
            'company': 'Sony PlayStation',
            'date': '2011',
            'description': '77 millions de comptes compromis',
            'impact': 'Informations personnelles, adresses, données de connexion'
        },
        {
            'company': 'Capital One',
            'date': '2019',
            'description': '106 millions de clients affectés',
            'impact': 'Numéros de sécurité sociale, comptes bancaires'
        },
        {
            'company': 'Twitter',
            'date': '2022',
            'description': '5.4 millions de comptes exposés',
            'impact': 'Emails, numéros de téléphone'
        }
    ]
    
    def get_all_news(self):
        """
        Retourne toutes les news de hacks.
        
        Returns:
            list: Liste des incidents de sécurité
        """
        return self.HACKED_COMPANIES
    
    def get_latest_news(self, count=5):
        """
        Retourne les dernières news.
        
        Args:
            count: Nombre de news à retourner
            
        Returns:
            list: Liste des derniers incidents
        """
        return self.HACKED_COMPANIES[:count]
    
    def search_by_company(self, company_name):
        """
        Recherche des incidents pour une entreprise spécifique.
        
        Args:
            company_name: Nom de l'entreprise
            
        Returns:
            list: Liste des incidents pour cette entreprise
        """
        return [
            incident for incident in self.HACKED_COMPANIES
            if company_name.lower() in incident['company'].lower()
        ]
    
    def format_news(self, incident):
        """
        Formate un incident de sécurité pour l'affichage.
        
        Args:
            incident: Dictionnaire représentant un incident
            
        Returns:
            str: Incident formaté
        """
        return f"""
╔════════════════════════════════════════════════════════════════
║ {incident['company']} ({incident['date']})
╠════════════════════════════════════════════════════════════════
║ Description: {incident['description']}
║ Impact: {incident['impact']}
╚════════════════════════════════════════════════════════════════
"""
    
    def display_all_news(self):
        """Affiche toutes les news de manière formatée."""
        print("\n" + "="*70)
        print(" 🚨 ENTREPRISES VICTIMES DE HACKS - HISTORIQUE 🚨 ")
        print("="*70 + "\n")
        
        for incident in self.HACKED_COMPANIES:
            print(self.format_news(incident))
        
        print(f"\nTotal: {len(self.HACKED_COMPANIES)} incidents majeurs recensés")
        print("\n⚠️  Utilisez toujours des mots de passe forts et uniques!")
