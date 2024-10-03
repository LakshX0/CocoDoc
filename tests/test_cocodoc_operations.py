import unittest
from unittest.mock import patch, MagicMock
import numpy as np
import mysql.connector
from cocodoc import create_connection, preprocess_image, fetch_dashboard_data, save_prediction_to_db

class TestCocoDocOperations(unittest.TestCase):

    # Test for Database connection
    @patch('your_module_name.mysql.connector.connect')
    def test_create_connection(self, mock_connect):
        # Mock the MySQL connection
        mock_connect.return_value = MagicMock()
        conn = create_connection()
        self.assertTrue(conn)

    # Test for Image Preprocessing
    def test_preprocess_image(self):
        from PIL import Image
        # Create a dummy image of size 500x500
        dummy_image = Image.new('RGB', (500, 500), 'green')
        processed_image = preprocess_image(dummy_image)
        
        # Check that the image is resized to (224, 224)
        self.assertEqual(processed_image.shape, (1, 224, 224, 3))

    # Test prediction saving to the database
    @patch('your_module_name.create_connection')
    def test_save_prediction_to_db(self, mock_conn):
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        
        # Call the function to save a prediction
        save_prediction_to_db("WCLWD", 0.85, 1, "leaf_image.jpg")
        
        # Verify if the insert query was executed
        mock_cursor.execute.assert_called_once()
        mock_cursor.close.assert_called_once()

    # Test Dashboard Data Fetching
    @patch('your_module_name.create_connection')
    def test_fetch_dashboard_data(self, mock_conn):
        # Mock the MySQL connection and cursor
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        
        # Mock data for predictions
        mock_cursor.fetchone.side_effect = [{"total_predictions": 100}]
        mock_cursor.fetchall.side_effect = [
            [{"predicted_class": "WCLWD", "count": 60}, {"predicted_class": "Healthy Leaves", "count": 40}],
            [{"timestamp": "2024-01-01 12:00:00", "predicted_class": "WCLWD", "confidence": 0.92, "is_healthy": 0}]
        ]
        
        # Call the function to fetch data
        total_predictions, disease_counts, recent_predictions = fetch_dashboard_data()
        
        # Assertions to check data
        self.assertEqual(total_predictions, 100)
        self.assertEqual(disease_counts[0]["predicted_class"], "WCLWD")
        self.assertEqual(recent_predictions[0]["predicted_class"], "WCLWD")

# Run the tests
if __name__ == '__main__':
    unittest.main()
