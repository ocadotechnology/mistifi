


import getpass
import sys
import time
import yaml
import json

import requests
from requests.adapters import HTTPAdapter

import logging
import logzero
from logzero import logger



class MistCloud:


    # All AOS8 API resources are found on the MM https://<MM-IP>:4343/api

    def __init__(self, token):
        self.token = token

        # Organisation is what's under the MSP
        #self.org_id = str()
        #self.site_id = str()


        # Mist Base API URL
        self.mist_base_api_url = "https://api.mist.com/api/v"

        # Setup the headder with the Authorisation token
        self.headers = {
            'Content-Type': 'application/json',
            'Accept' : 'application/json',
            'Authorization': 'Token {}'.format(self.token),
        }


        # Make a session and limit retries
        self.session = requests.Session()
        self.session.mount(self.mist_base_api_url, HTTPAdapter(max_retries=3))



    def expand_url(self, org_id=None, site_id=None, resource=None, api_version=1):
        '''
        Creates  a Mist URL using the given components.

        Args:
            org_id (str, optional):
                The organisation id.
                If specified, this will be incorporated into the URL as /api/v1/orgs/:org_id
            site_id (str, optional):
                The site id.
                If specified, this will be incorporated into the URL as either:
                - api/v1/sites/:site_id OR
                - api/v1/orgs/:org_id/sites/:site_id if org_id is specified
            resource (str, optional):
                The resource to retrieve.
                You can specify just this object, but must include everything after the .
            api_version (int, optional):
                Which Mist API version to use.
                Default: 1.

        Returns:
            str:
                The expanded URL.
                Examples:
                
                expand_url(resource='/const/ap_channels') returns
                https://api.mist.com/api/v1/const/ap_channels

                expand_url(org_id="93a28cf5-2b40-40a7-97d3-05ed23f43682", resource='/wlans') returns
                https://api.mist.com/api/v1/orgs/93a28cf5-2b40-40a7-97d3-05ed23f43682/wlans
        '''

        # Start with the base URL and API version
        url = self.mist_base_api_url + str(api_version)
        

        if org_id:
            url += '/orgs/{}'.format(org_id)

        if site_id:
            url += '/sites/{}'.format(site_id)

        if resource and resource[0] == "/":
            url += resource
        else: 
            url+= "/{}".format(resource)

        #getpass('\n>>> Built URL:\n\t{}\nPress ENTER to continue..\n'.format(url))
        return url



    def get(self, org_id=None, site_id=None, resource=None, api_version=1, **get_params):

        expanded_url = self.expand_url(org_id=org_id, site_id=site_id, resource=resource)

        try:
            resp = requests.get(expanded_url, headers=self.headers, params=get_params)
            resp.raise_for_status()
        except Exception as e:
            logging.exception("Problem with URL: {}\n".format(e.args[0]))
            #logging.error("Response headers {}\n".format(resp.headers))
            #logging.error("Request headers {}".format(resp.request.headers))
        else:
            jresp = json.loads(resp.text)
            return(jresp)


    def put(self, org_id=None, site_id=None, resource=None, api_version=1, jdata=None):

        expanded_url = self.expand_url(org_id=org_id, site_id=site_id, resource=resource)


        try:
            resp = requests.put(expanded_url, headers=self.headers, json=jdata)
            resp.raise_for_status()
        except requests.HTTPError as e:
            logging.exception("Problem with URL: {}\n".format(e.args[0]))
        else:
            jresp = json.loads(resp.text)
            return(jresp)



    def post(self):
        expanded_url = self.expand_url(org_id=org_id, site_id=site_id, resource=resource)


        try:
            resp = requests.post(expanded_url, headers=self.headers, json=jdata)
            resp.raise_for_status()
        except requests.HTTPError as e:
            logging.exception("Problem with URL: {}\n".format(e.args[0]))
        else:
            jresp = json.loads(resp.text)
            return(jresp)

    def delete(self):
        pass


    def create_site(self):
        pass
