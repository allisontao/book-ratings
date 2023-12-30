import unittest
from unittest.mock import patch
import pandas as pd
from main import normalize_titles, process_ratings, read_database, write_data

class TestYourScript(unittest.TestCase):

    def test_normalize_titles(self):
        self.assertEqual(normalize_titles("the great gatsby"), "The Great Gatsby")
        self.assertEqual(normalize_titles("harry potter and the sorcerer's stone"), "Harry Potter And The Sorcerer's Stone")

    def test_process_ratings(self):
        data = {
        'book_title': ['Book 1', 'Book 1', 'Book 2', 'Book 1', 'Book 2'],
        'member': ['Lauren O', 'Lauren O', 'Jordan S', 'David B', 'David B'],
        'book_rating': [4, 5, 3, 3.5, 5]
        }
        df = pd.DataFrame(data)
        result_df = process_ratings(df)
        self.assertEqual(result_df.shape[0], 2)
        self.assertEqual(result_df.loc[result_df['book_title'] == 'Book 1', 'average_rating'].values[0], 4.25)
        self.assertEqual(result_df.loc[result_df['book_title'] == 'Book 1', 'favorites'].values[0], 1)
        self.assertEqual(result_df.loc[result_df['book_title'] == 'Book 2', 'average_rating'].values[0], 4)
        self.assertEqual(result_df.loc[result_df['book_title'] == 'Book 2', 'favorites'].values[0], 1)
      
    def test_read_database(self):
        with patch('main.notion.databases.query') as mock_query:
            read_database()
        mock_query.assert_called_once_with("2e807af3c29548c5887c35e1456c003d")
    
    # Test that a new record will be created if the book title does not exist already in the database    
    def test_write_data_not_in_existing_books(self):
        row = {'book_title': 'New Book', 'average_rating': 4, 'favorites': 10}
        existing_book_titles = ['Book 1', 'Book 2']

        with patch('main.notion.pages.create') as mock_create:
            write_data(row, existing_book_titles)

        mock_create.assert_called_once_with(
            parent={'database_id': '2e807af3c29548c5887c35e1456c003d'},
            properties={
                'Book Title': {'title': [{'text': {'content': 'New Book'}}]},
                'Rating': {'number': 4},
                'Favorites': {'number': 10}
            }
        )
        
    # Test that a new record will not be created if the book title already exists in the database    
    def test_write_data_in_existing_books(self):
        row = {'book_title': 'Book 1', 'average_rating': 4, 'favorites': 10}
        existing_book_titles = ['Book 1', 'Book 2']

        with patch('main.notion.pages.create') as mock_create:
            write_data(row, existing_book_titles)

        mock_create.assert_not_called()
        

if __name__ == '__main__':
    unittest.main()
