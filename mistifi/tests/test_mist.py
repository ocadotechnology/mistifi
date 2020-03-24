import os
import sys
import json
import responses
import requests
import unittest

sys.path.append(os.path.dirname(__file__) + '../')
#print(sys.path)

from ..mistifi import MistiFi
from .test_data.test_data import *

LOGIN_URL = 'https://api.mist.com/api/v1/login'


class TestMistiFi(unittest.TestCase):
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
        #assert resp.json() == login_resp

        self.mist = MistiFi(token='careparetoken')
        self.mist.comms()

    def test__resource_url(self):
        '''Test for _resource_url() 

        For propper URL formatting
        
        Examples of URLs that should be built
        /api/v1/sites/:site_id/wlans
        /api/v1/sites/:site_id/wlans/:wlan_id
        /api/v1/sites/:site_id/wlans/:wlan_id/parameter
        /api/v1/sites/:site_id/wlans/derived
        '''
        expected_url = 'https://api.mist.com/api/v1'
        actual_url = self.mist._resource_url()
        self.assertEqual(expected_url, actual_url)

        # 
        ## Testing URI
        #

        # If specifying URI it should be in there after v1
        expected_url = 'https://api.mist.com/api/v1/wlans'
        actual_url = self.mist._resource_url(uri='wlans')
        self.assertEqual(expected_url, actual_url)

        # Lower or upper case parameter doesn't matter
        expected_url = 'https://api.mist.com/api/v1/wlans'
        actual_url = self.mist._resource_url(URI='wlans')
        self.assertEqual(expected_url, actual_url)

        # URI parameter will be first even if some other is passed in before it
        expected_url = 'https://api.mist.com/api/v1/wlans/parameter'
        actual_url = self.mist._resource_url(parameter='parameter', uri='wlans')
        self.assertEqual(expected_url, actual_url)

        # 
        ## Testing various IDs
        #

        # Having any ID in the url builds the URL to ...v1//xxx/:ID like below 
        expected_url = 'https://api.mist.com/api/v1/sites/:site_id123'
        actual_url = self.mist._resource_url(site_id=':site_id123')
        self.assertEqual(expected_url, actual_url)

        # ID can have a leading '/' but not a trailing one
        expected_url = 'https://api.mist.com/api/v1/sites/:site_id123'
        actual_url = self.mist._resource_url(site_id='/:site_id123')
        self.assertEqual(expected_url, actual_url)

        # If IDs have a trailing '/' it will cause the URL to
        # NOT be built correctly
        expected_url = 'https://api.mist.com/api/v1/sites/:site_id123'
        actual_url = self.mist._resource_url(site_id=':site_id123/')
        self.assertEqual(expected_url, actual_url)

        expected_url = 'https://api.mist.com/api/v1/sites/:site_id123'
        actual_url = self.mist._resource_url(site_id='/:site_id123/')
        self.assertEqual(expected_url, actual_url)

        expected_url = 'https://api.mist.com/api/v1/orgs/:org_id123'
        actual_url = self.mist._resource_url(org_id=':org_id123')
        self.assertEqual(expected_url, actual_url)

        # IDs are organised so that first comes org_id, then site_id, 
        # then the rest irrespective of the order they've been passed in
        expected_url = 'https://api.mist.com/api/v1/orgs/:org_id123/sites/:site_id123/wlans/:wlan_id123'
        actual_url = self.mist._resource_url(
            wlan_id=':wlan_id123', 
            site_id='/:site_id123/', 
            org_id=':org_id123')
        self.assertEqual(expected_url, actual_url)


        # 
        ## Testing for adding endpoint parameters (not same as params)
        #
        expected_url = 'https://api.mist.com/api/v1/sites/:site_id123/wlans/:wlan_id123/parameter'
        actual_url = self.mist._resource_url(
            site_id=':site_id123', 
            wlan_id=':wlan_id123', 
            parameter='/parameter')
        self.assertEqual(expected_url, actual_url)

        expected_url = 'https://api.mist.com/api/v1/sites/:site_id123/wlans/:wlan_id123/parameter'
        actual_url = self.mist._resource_url(
            site_id=':site_id123', 
            wlan_id=':wlan_id123', 
            parameter='/parameter/')
        self.assertEqual(expected_url, actual_url)

        expected_url = 'https://api.mist.com/api/v1/sites/:site_id123/wlans/:wlan_id123/parameter'
        actual_url = self.mist._resource_url(
            site_id=':site_id123', 
            wlan_id=':wlan_id123', 
            parameter='parameter')
        self.assertEqual(expected_url, actual_url)

        # parameters can be any key
        expected_url = 'https://api.mist.com/api/v1/sites/:site_id123/wlans/:wlan_id123/parameter'
        actual_url = self.mist._resource_url(
            site_id=':site_id123', 
            wlan_id=':wlan_id123', 
            blah1='/parameter')
        self.assertEqual(expected_url, actual_url)

        expected_url = 'https://api.mist.com/api/v1/sites/:site_id123/wlans/:wlan_id123/parameter1/parameter2'
        actual_url = self.mist._resource_url(
            site_id=':site_id123', 
            wlan_id=':wlan_id123', 
            blah1='/parameter1', 
            blah2='/parameter2')
        self.assertEqual(expected_url, actual_url)

    def test__params(self):
        '''Test for _params()
        '''
        expected_params = {'param1':'value1'}
        actual_params = self.mist._params(site_id=':site_id123', params={'param1':'value1'})
        self.assertEqual(expected_params, actual_params)

        expected_params = {'param1':'value1', 'param2': 'value2'}
        actual_params = self.mist._params(site_id=':site_id123', params={'param1':'value1', 'param2': 'value2'})
        self.assertEqual(expected_params, actual_params)


if __name__ == '__main__':
    unittest.main()




