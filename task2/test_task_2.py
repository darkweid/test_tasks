import unittest
from unittest.mock import patch, Mock
from bs4 import BeautifulSoup
from solution import (
    is_cyrillic_letter,
    get_animals_from_page,
    get_next_page_url,
    count_animals_by_letter,
    save_to_csv
)
import os
import tempfile


class TestAnimalCounter(unittest.TestCase):
    def setUp(self):
        self.sample_html = """
        <div id="mw-pages">
            <div class="mw-category">
                <div class="mw-category-group">
                    <ul>
                        <li><a href="/wiki/Аист">Аист</a></li>
                        <li><a href="/wiki/Барс">Барс</a></li>
                        <li><a href="/wiki/Волк">Волк</a></li>
                    </ul>
                </div>
            </div>
            <a href="/next_page">Следующая страница</a>
        </div>
        """
        self.soup = BeautifulSoup(self.sample_html, 'html.parser')

    def test_is_cyrillic_letter(self):
        """Test Cyrillic letter detection"""
        self.assertTrue(is_cyrillic_letter('А'))
        self.assertTrue(is_cyrillic_letter('Я'))
        self.assertTrue(is_cyrillic_letter('а'))  # lowercase
        self.assertFalse(is_cyrillic_letter('A'))  # Latin A
        self.assertFalse(is_cyrillic_letter('1'))
        self.assertFalse(is_cyrillic_letter(' '))

    @patch('requests.get')
    def test_get_animals_from_page(self, mock_get):
        """Test getting animals from a page"""
        # Mock the response
        mock_response = Mock()
        mock_response.text = self.sample_html
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        animals, has_more = get_animals_from_page('http://test.com')

        self.assertEqual(len(animals), 3)
        self.assertEqual(animals, ['Аист', 'Барс', 'Волк'])
        self.assertTrue(has_more)
        mock_get.assert_called_once_with('http://test.com')

    @patch('requests.get')
    def test_get_animals_from_page_with_mixed_alphabet(self, mock_get):
        """Test getting animals when there's a mix of Cyrillic and Latin letters"""
        mixed_html = """
        <div id="mw-pages">
            <div class="mw-category">
                <div class="mw-category-group">
                    <ul>
                        <li><a href="/wiki/Аист">Аист</a></li>
                        <li><a href="/wiki/Барс">Барс</a></li>
                        <li><a href="/wiki/Cat">Cat</a></li>
                    </ul>
                </div>
            </div>
        </div>
        """
        mock_response = Mock()
        mock_response.text = mixed_html
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        animals, has_more = get_animals_from_page('http://test.com')

        self.assertEqual(len(animals), 2)
        self.assertEqual(animals, ['Аист', 'Барс'])
        self.assertFalse(has_more)

    def test_get_next_page_url(self):
        """Test next page URL extraction"""
        base_url = 'https://ru.wikipedia.org'
        next_url = get_next_page_url(self.soup, base_url)
        self.assertEqual(next_url, 'https://ru.wikipedia.org/next_page')

    def test_get_next_page_url_no_next_page(self):
        """Test when there is no next page"""
        soup = BeautifulSoup('<div></div>', 'html.parser')
        next_url = get_next_page_url(soup, 'https://ru.wikipedia.org')
        self.assertIsNone(next_url)

    @patch('solution.get_animals_from_page')
    @patch('requests.get')
    def test_count_animals_by_letter(self, mock_get, mock_get_animals):
        """Test counting animals by first letter"""
        # Mock the responses
        mock_response = Mock()
        mock_response.text = self.sample_html
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # Mock get_animals_from_page to return test data
        mock_get_animals.side_effect = [
            (['Аист', 'Антилопа', 'Барс'], True),
            (['Волк', 'Ворона'], False)
        ]

        result = count_animals_by_letter()

        self.assertEqual(result['А'], 2)
        self.assertEqual(result['Б'], 1)
        self.assertEqual(result['В'], 2)

    def test_save_to_csv(self):
        """Test saving data to CSV"""
        test_data = {'А': 2, 'Б': 1, 'В': 3}

        # Use temporary file for testing
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.csv') as tmp:
            save_to_csv(test_data, tmp.name)

            # Read and check the contents
            tmp.seek(0)
            contents = tmp.read()

            self.assertIn('А,2', contents)
            self.assertIn('Б,1', contents)
            self.assertIn('В,3', contents)

        # Cleanup
        os.unlink(tmp.name)

    def test_save_to_csv_error_handling(self):
        """Test error handling when saving CSV"""
        test_data = {'А': 2, 'Б': 1}

        # Try to save to an invalid location
        with self.assertRaises(Exception):
            save_to_csv(test_data, '/invalid/path/test.csv')


if __name__ == '__main__':
    unittest.main()