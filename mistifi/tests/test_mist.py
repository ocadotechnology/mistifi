import os
import json
import responses
import requests
import unittest

sys.path.append(os.path.dirname(__file__) + "/../")
#print(sys.path)

from mistifi import Mistifi
from .test_data.test_data import *

LOGIN_URL = "https://api.mist.com/api/v1/login"


class TestMistyFi(unittest.TestCase):
    '''Test class for testing Mist APIs.
    '''
    @responses.activate
    def setUp(self):
        '''Mist API client instance creator for the whole class.
        '''
        responses.add(
            responses.POST, 
            LOGIN_URL, 
            status=200, 
            json=login_resp)

        resp = requests.post(LOGIN_URL)
        
        # For figuring out how to use responses
        assert resp.json() == login_resp

        self.mist = MistiFi("us", "care", "pare")
        self.mist.comms()

    def test_urls(self):
        '''Test for propper URL formatting
        '''
        expected_url = 'configuration/object/ap_sys_prof'

        actual_url = self.mist._kwargs_modify('configuration/object/ap_sys_prof')

        self.assertEqual(
            expected_kwargs, 
            actual_kwargs, 
            f'\nExp kwargs = {expected_kwargs}\nAct kwargs = {actual_kwargs}')

if __name__ == "__main__":
    unittest.main()




