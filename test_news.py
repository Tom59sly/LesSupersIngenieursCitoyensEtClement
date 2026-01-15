"""
Tests pour le module de news.
"""
import unittest
from news import HackNewsDatabase


class TestHackNewsDatabase(unittest.TestCase):
    """Tests pour la classe HackNewsDatabase."""
    
    def setUp(self):
        """Initialise la base de données pour chaque test."""
        self.news_db = HackNewsDatabase()
    
    def test_get_all_news(self):
        """Test la récupération de toutes les news."""
        all_news = self.news_db.get_all_news()
        self.assertIsInstance(all_news, list)
        self.assertGreater(len(all_news), 0)
    
    def test_get_latest_news(self):
        """Test la récupération des dernières news."""
        latest = self.news_db.get_latest_news(3)
        self.assertEqual(len(latest), 3)
        
        latest = self.news_db.get_latest_news(5)
        self.assertEqual(len(latest), 5)
    
    def test_search_by_company_found(self):
        """Test la recherche d'une entreprise existante."""
        results = self.news_db.search_by_company("Yahoo")
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0]['company'], 'Yahoo')
    
    def test_search_by_company_not_found(self):
        """Test la recherche d'une entreprise inexistante."""
        results = self.news_db.search_by_company("EntrepriseInconnue")
        self.assertEqual(len(results), 0)
    
    def test_search_case_insensitive(self):
        """Test que la recherche est insensible à la casse."""
        results_lower = self.news_db.search_by_company("yahoo")
        results_upper = self.news_db.search_by_company("YAHOO")
        results_mixed = self.news_db.search_by_company("Yahoo")
        
        self.assertEqual(len(results_lower), len(results_upper))
        self.assertEqual(len(results_lower), len(results_mixed))
    
    def test_incident_structure(self):
        """Test la structure d'un incident."""
        all_news = self.news_db.get_all_news()
        for incident in all_news:
            self.assertIn('company', incident)
            self.assertIn('date', incident)
            self.assertIn('description', incident)
            self.assertIn('impact', incident)
    
    def test_format_news(self):
        """Test le formatage d'un incident."""
        incident = {
            'company': 'Test Company',
            'date': '2023',
            'description': 'Test description',
            'impact': 'Test impact'
        }
        formatted = self.news_db.format_news(incident)
        
        self.assertIn('Test Company', formatted)
        self.assertIn('2023', formatted)
        self.assertIn('Test description', formatted)
        self.assertIn('Test impact', formatted)


if __name__ == '__main__':
    unittest.main()
