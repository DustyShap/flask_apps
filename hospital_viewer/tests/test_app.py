#! /usr/bin/env python3

"""
    A tester to verify correctness of various RESTful endpoints of the hospital
    JSON viewer app.

    Author: James Matsumura
"""

import urllib.request
import unittest
import json
import os

api_loc = os.getenv('HOSPITAL_API', 'http://localhost:5000')

class TestHospitalAPI(unittest.TestCase):

    def test_first_record(self):
        """
        Verifies the first hospital record is correct. 
        """

        first_hospital = {
            "address": "251 E Huron St", 
            "city": "Chicago", 
            "id": 1, 
            "name": "Northwestern Memorial Hospital", 
            "state": "IL"
        }

        req = urllib.request.urlopen('{}/hospitals/1'.format(api_loc))
        json_representation = json.loads(req.read().decode('utf-8'))

        self.assertEqual(json_representation, first_hospital)

    def test_missing_record(self):
        """
        Verifies that a nonexistent record returns nicely. 
        """

        record_id = 1000000

        missing_hospital = {
            'message': 'No hospital with ID = {}'.format(record_id)
        }

        req = urllib.request.urlopen('{}/hospitals/{}'.format(api_loc,record_id))
        json_representation = json.loads(req.read().decode('utf-8'))

        self.assertEqual(json_representation, missing_hospital)

    def test_post_endpoint(self):
        """
        Verifies that a POST to an existing ID fails. 
        """

        first_hospital = [{
            "address": "251 E Huron St", 
            "city": "Chicago", 
            "id": 1, 
            "name": "Northwestern Memorial Hospital", 
            "state": "IL"
        }]
        
        req = urllib.request.Request('{}/hospitals'.format(api_loc), 
            data=json.dumps(first_hospital).encode('utf-8'),
            headers={'content-type': 'application/json'}
        )

        response = urllib.request.urlopen(req)
        json_representation = json.loads(response.read().decode('utf-8'))

        self.assertEqual(json_representation['conflicting_keys'][0], 1)


if __name__ == '__main__':
    unittest.main()