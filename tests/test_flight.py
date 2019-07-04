"""Test case for the user functionality"""
import os
import json

from app import create_app, db
from app.auth.models import User
from tests.base_test import BaseTestCase


class TestAirportManipulation(BaseTestCase):
    """Test for Airport manipulation endpoint"""
    def test_admin_airport_addition(self):
        """Test adding airport by admin works correcty"""
        self.admin_login()
        res = self.client.post('api/airport',
                               headers=self.header,
                               data=json.dumps(self.airport_data))
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'],
                         "Airport registered successfully")
        self.assertEqual(res.status_code, 201)

    def test_user_airport_addition(self):
        """Test adding airport by user is not possible"""
        self.get_login_token()
        res = self.client.post('api/airport',
                               headers=self.header,
                               data=json.dumps(self.airport_data))
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'],
                         "Forbidden, Admins only!")
        self.assertEqual(res.status_code, 403)

    def test_get_available_airports(self):
        """Test get all available airports"""
        self.admin_login()
        self.client.post('api/airport',
                         headers=self.header,
                         data=json.dumps(self.airport_data))
        res = self.client.get('api/airport',
                              headers=self.header)
        result = json.loads(res.data.decode())
        self.assertEqual(result['number_of_airports'], 1)
        self.assertEqual(res.status_code, 200)

    def test_get_no_airports(self):
        """Test get all airports before adding"""
        self.admin_login()
        res = self.client.get('api/airport',
                              headers=self.header)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "No data to display")
        self.assertEqual(res.status_code, 200)
