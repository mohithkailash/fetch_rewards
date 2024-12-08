import unittest
import json
from rules import (
    calculate_points, 
    get_retailer_points, 
    get_round_dollar_points,
    get_multiple_of_quarter_points,
    get_items_pairs_points,
    get_description_length_points,
    get_odd_day_points,
    get_time_range_points
)
from app import app
from datetime import datetime

class TestReceiptProcessor(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.base_receipt = {
            "retailer": "Test Store",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {
                    "shortDescription": "Item 1",
                    "price": "10.00"
                }
            ],
            "total": "10.00"
        }

    def test_retailer_points(self):
        test_cases = [
            ("Target", 6),
            ("Target ", 6),
            ("M&M Corner Market", 14),
            ("123 Store!", 8),
            # ("123 Store!", 9), # must fail
            ("A&P", 2),
            ("    Spaces    ", 6)
        ]
        for retailer, expected in test_cases:
            points = get_retailer_points(retailer)
            self.assertEqual(points, expected, f"Failed for retailer: {retailer}")

    def test_round_dollar_points(self):
        test_cases = [
            ("100.00", 50),
            ("99.99", 0),
            ("0.00", 50),
            ("10.50", 0)
        ]
        for total, expected in test_cases:
            points = get_round_dollar_points(total)
            self.assertEqual(points, expected, f"Failed for total: {total}")

    def test_quarter_multiple_points(self):
        test_cases = [
            ("100.00", 25),
            ("99.75", 25),
            ("99.99", 0),
            ("0.00", 25),
            ("10.50", 25)
        ]
        for total, expected in test_cases:
            points = get_multiple_of_quarter_points(total)
            self.assertEqual(points, expected, f"Failed for total: {total}")

    def test_items_pair_points(self):
        test_items = [{"shortDescription": "Test Item", "price": "10.00"}]
        test_cases = [
            (1, 0),    # No pairs
            (2, 5),    # One pair
            (3, 5),    # One pair + 1
            (4, 10),   # Two pairs
            (5, 10),   # Two pairs + 1
            (10, 25)   # Five pairs
        ]
        for count, expected in test_cases:
            items = test_items * count
            points = get_items_pairs_points(items)
            self.assertEqual(points, expected, f"Failed for {count} items")

    def test_description_length_points(self):
        test_cases = [
            ([{"shortDescription": "abc", "price": "10.00"}], 2),
            ([{"shortDescription": "abcd", "price": "10.00"}], 0),
            ([{"shortDescription": "abcdef", "price": "10.00"}], 2),
            ([{"shortDescription": "   abc   ", "price": "10.00"}], 2),
            ([{"shortDescription": "ab c", "price": "10.00"}], 0)
        ]
        for items, expected in test_cases:
            points = get_description_length_points(items)
            self.assertEqual(points, expected, f"Failed for description: {items[0]['shortDescription']}")

    def test_odd_day_points(self):
        test_cases = [
            ("2022-01-01", 6),  # Odd day
            ("2022-01-02", 0),  # Even day
            ("2022-01-31", 6),  # Odd day
            ("2022-02-28", 0)   # Even day
        ]
        for date, expected in test_cases:
            points = get_odd_day_points(date)
            self.assertEqual(points, expected, f"Failed for date: {date}")

    def test_time_range_points(self):
        test_cases = [
            ("13:59", 0),   # Before 2 PM
            ("14:00", 10),  # At 2 PM
            ("15:30", 10),  # Between 2-4 PM
            ("16:00", 10),  # At 4 PM
            ("16:01", 0)    # After 4 PM
        ]
        for time, expected in test_cases:
            points = get_time_range_points(time)
            self.assertEqual(points, expected, f"Failed for time: {time}")

    def test_integration(self):
        example_receipt1 = {
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {
                    "shortDescription": "Mountain Dew 12PK",
                    "price": "6.49"
                },{
                    "shortDescription": "Emils Cheese Pizza",
                    "price": "12.25"
                },{
                    "shortDescription": "Knorr Creamy Chicken",
                    "price": "1.26"
                },{
                    "shortDescription": "Doritos Nacho Cheese",
                    "price": "3.35"
                },{
                    "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
                    "price": "12.00"
                }
            ],
            "total": "35.35"
        }
        
        example_receipt2 = {
            "retailer": "M&M Corner Market",
            "purchaseDate": "2022-03-20",
            "purchaseTime": "14:33",
            "items": [
                {
                    "shortDescription": "Gatorade",
                    "price": "2.25"
                },{
                    "shortDescription": "Gatorade",
                    "price": "2.25"
                },{
                    "shortDescription": "Gatorade",
                    "price": "2.25"
                },{
                    "shortDescription": "Gatorade",
                    "price": "2.25"
                }
            ],
            "total": "9.00"
        }

        self.assertEqual(calculate_points(example_receipt1), 28)
        self.assertEqual(calculate_points(example_receipt2), 109)

    def test_api_endpoints(self):
        """Test API endpoints functionality"""
        # Test process endpoint
        response = self.app.post('/receipts/process', 
                               json=self.base_receipt,
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('id', data)
        
        # Test points endpoint
        points_response = self.app.get(f'/receipts/{data["id"]}/points')
        self.assertEqual(points_response.status_code, 200)
        self.assertIn('points', json.loads(points_response.data))

if __name__ == '__main__':
    unittest.main()