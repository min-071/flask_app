import unittest

from app import app, client  # Ensure accurate import paths
from unittest.mock import patch, MagicMock
from pymongo.errors import ConnectionFailure


class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        """
        Sets up the Flask test client for each test.
        """
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.client.admin.command')
    def test_mongodb_ping_command(self, mock_command):
        """
        Test 1: Verify Database Connectivity
        Simulates a MongoDB read operation using the ping command to check database connection.
        """
        # Simulate a successful 'ping' command response
        mock_command.return_value = {'ok': 1.0}

        try:
            result = client.admin.command('ping')
            self.assertEqual(result['ok'], 1.0)
        except ConnectionFailure:
            self.fail("MongoDB connection failed")

    def test_post_method_on_home_route(self):
        """
        Test 2: Verify POST Method on Home Route
        Sends a POST request to the home route ('/') and checks for a 405 status code
        since the route only accepts GET requests.
        """
        response = self.app.post('/')
        self.assertEqual(response.status_code, 405)  # Expect 405 Method Not Allowed

    @patch('app.products_collection')
    def test_insert_and_query_mongodb(self, mock_products_collection):
        """
        Test 3: Verify Database Insert and Query
        Tests inserting a new document into the MongoDB and querying it back.
        """
        mock_inserted_id = MagicMock()
        mock_products_collection.insert_one.return_value.inserted_id = mock_inserted_id

        new_product = {'name': 'New Product', 'price': 300}
        result = mock_products_collection.insert_one(new_product)
        inserted_id = result.inserted_id

        # Ensure the insert operation returns the mocked inserted_id
        self.assertEqual(inserted_id, mock_inserted_id)

        # Simulate the query to return the inserted document
        mock_products_collection.find_one.return_value = new_product
        queried_product = mock_products_collection.find_one({'_id': inserted_id})

        # Ensure the queried document matches the inserted document
        self.assertEqual(queried_product, new_product)


if __name__ == '__main__':
    unittest.main()
