import getpass
import sys
import time
import yaml
import json

import requests
from requests import Request, Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from urllib.parse import urlparse, urljoin

import logging
import logzero
from logzero import logger


import http

clouds = {
    "US": "api.mist.com",
    "EU": "api.eu.mist.com",
}

class MistiFi:
    '''All Mist API uris are found on https://api.mist.com/api/v1/docs/Home, and are accessible if logged in'''

    def __init__(self, cloud="us", token=None, username=None, password=None, user_token=None, apiv=1, verify=False, timeout=10, debug=False):

        # Set logging to ERROR to not display anything by default
        if debug:
            logzero.loglevel(logging.DEBUG)
            #http.client.HTTPConnection.debuglevel = 1
        else:
            logzero.loglevel(logging.ERROR)
            http.client.HTTPConnection.debuglevel = 0


        self.token = token
        self.username = username
        self.password = password
        self.user_token = user_token
        self.verify = bool(verify)
        self.timeout = abs(timeout)
        self.apiv = apiv
        self.csrftoken = None


        self.cloud = self._select_cloud(cloud)
        logger.debug(f"Selected cloud: '{self.cloud}' >> '{cloud.upper()}'")
        #try:
        #    self.cloud = clouds[cloud.upper()]
        #except KeyError:
        #    logging.exception(f'Not a valid entry {list(clouds.keys())}. Using "US" as default.')
        #    self.cloud = clouds["US"]

        self.mist_base_api_url = f'https://{self.cloud}/'
        logger.debug(f'Base URL: {self.mist_base_api_url}')

        # Configure the session
        #self._config_session()

        '''
        #
        # If token provided, use it to log into the Mist cloud...
        #
        if token:
            self.token = token
            self.headers['Authorization'] = f'Token {self.token}'

        # ...otherwise prompt for user credentials if not provided
        else:
            #
            # If username not provided, ask for it
            #
            self.login_payload = {"email": None, "password": None}

            if not self.username:
                user_input = input("Mist username required. Should I use `{}` to continue [Y/n]?".format(getpass.getuser()))

                # Option for a user if they want to specify a username
                if user_input.lower() == "n":
                    #kwargs.update({ 'username': input("Username:\x20") })
                    self.username = input("Username:\x20")
                # ...any other answer, just use their current username
                else:
                    self.username = getpass.getuser()

            self.login_payload['email'] = self.username

            #
            # If password not provided, ask for it
            #
            if not self.password:
                #
                # If password was not provided, get it from user input
                self.password = getpass.getpass(f"Mist password for user `{self.username}` required:\x20".format(self.username))
            
            # Then set it in the login payload outside of conditional
            # as the password might have been passed in with the object
            self.login_payload['password'] = self.password

            # Finaly login
            self._user_login(self.login_payload)

        # Reset the log level to ERROR only
        logzero.loglevel(logging.ERROR)
        '''
    def login(self):

        logger.info(f'Calling communicate()')

        # Configure the session
        self._config_session()

        #
        # If token provided, use it to log into the Mist cloud...
        #
        if self.token:
            self.headers['Authorization'] = f'Token {self.token}'

        # ...otherwise prompt for user credentials if not provided
        else:
            #
            # If username not provided, ask for it
            #
            self.login_payload = {"email": None, "password": None}

            if not self.username:
                user_input = input("Mist username required. Should I use `{}` to continue [Y/n]?".format(getpass.getuser()))

                # Option for a user if they want to specify a username
                if user_input.lower() == "n":
                    #kwargs.update({ 'username': input("Username:\x20") })
                    self.username = input("Username:\x20")
                # ...any other answer, just use their current username
                else:
                    self.username = getpass.getuser()

            self.login_payload['email'] = self.username

            #
            # If password not provided, ask for it
            #
            if not self.password:
                #
                # If password was not provided, get it from user input
                self.password = getpass.getpass(f"Mist password for user `{self.username}` required:\x20".format(self.username))
            
            # Then set it in the login payload outside of conditional
            # as the password might have been passed in with the object
            self.login_payload['password'] = self.password

            # Finaly login
            self._user_login(self.login_payload)

        # Reset the log level to ERROR only
        logzero.loglevel(logging.ERROR)

    def _config_session(self):
        '''Session configurator for headers and requests.Session()'''

        logger.info(f'Calling _config_session()')

        # Setup base headers
        self.headers = {
            'Content-Type': 'application/json',
            'Accept' : 'application/json',
        }

        logger.debug(f'Updated Headers: {self.headers}')

        self.session = requests.Session() 

        # Setup the retry strategy
        # https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        self.session.mount(self.mist_base_api_url, HTTPAdapter(max_retries=retries))
        
        # Handle response status
        #assert_status_hook = lambda response, *args, **kwargs: response.raise_for_status()
        #self.session.hooks["response"] = [assert_status_hook]

    def _user_login(self, login_payload):
        '''Method to authenticate with username/password credentials. 

        Params:
        ------- 
        None
        
        Return:
        -------
        Nothing
        '''
        logger.info(f'Calling _user_login()')
        
        url_login = self._resource_url(uri='/login')
        #url_login = self._resource_url(org_id=':org_id')
        #url_login = self._resource_url(site_id=':site_id')
        #url_login = self._resource_url(site_id=':site_id', uri='/uri')
        #url_login = self._resource_url(org_id=":org_id", site_id=':site_id', uri='/uri')
        #url_login = self._resource_url(org_id=":org_id/orgA/", site_id=':site_id/siteA', uri='/uri')
        #url_login = self._resource_url(org_id="/:org_id/orgA/", site_id=':site_id/siteA', uri='/uri')
        #url_login = self._resource_url(somthing='/:sdkinvite_id/email',site_id=':site_id', uri='/uri')
        #url_login = self._resource_url(collection='/:collection',object_id=':obj_id',site_id=':site_id')
        #url_login = self._resource_url(somthing='/:sdkinvite_id/email',org_id=':org_id', uri='/uri')
        #url_login = self._resource_url(somthing='/:sdkinvite_id/email',org_id=":org_id", site_id=':site_id', uri='/uri')
        #url_login = self._resource_url(somthing='/:sdkinvite_id/email', blah="/blah", org_id=":org_id", site_id=':site_id', uri='/uri')
        #exit(0)

        # Login with or without the 2 factor token
        resp = self.session.post(url_login, json=login_payload)

        #resp = self._api_call("POST", url_login, json=login_payload)
        resp_head = resp.headers
        logger.info(f'Login response code: {resp.status_code}')
        logger.debug(f'Response HEAD: {resp_head}')
        
        # Need to split on ':' first and thake the first element, then split on '=' and take the second one
        try:
            self.csrftoken = resp.cookies['csrftoken']
        except KeyError:
            logger.exception("'Set-Cookie' not in headder response")
            return

        #self.headers['csrftoken'] = f"{csrf_token}"
        logger.debug(f'Updated Headers: {self.headers}')
        logger.debug(f'Response HEAD: {self.csrftoken}')

        # figure out how to incorporate 2FA. this below isn't it.
        #resp = whoami()
        #logger.debug(f'Self response: {resp.json()}')
        #logger.debug(f'Self head: {resp.headers}')

        return

        #if 'two_factor' in resp_head:
        #    url_2fa = self._resource_url("/api/v1/two_factor")
        #    resp = self._api_call("POST", url_2fa)
        #    logger.debug(f'Self data: {resp}')

    def _api_call(self, method, url, **kwargs):
        '''The API call handler.

        This method is used by `resource`. kwargs passed in get passed to the 
        requests.session instance

        Params
        ------
        method: `str`
            either `POST` or `GET`

        url: `str`
            URL with the endpoint included

        **kwargs: 
        These are passed into the requests and include the `params` and `json` 
        attributes which are the exact same ones as used by requests.

        Returns:
        --------
        The full response in JSON format including `_global_result` AND
        The error if status string returned is not 0, else `None`.
        '''
        logger.info("Calling _api_call()")
        logger.info(f"Method is: {method.upper()}")
        logger.info(f"Calling URL: {url}")
        logger.debug(f'With headers: {self.headers}')

        # This is where the call hapens
        response = getattr(self.session, method.lower())(url, cookies=dict(csrftoken=self.csrftoken), **kwargs)
        resp_head = response.headers

        logger.info(f"Response status code: {response.status_code}")

        # Return nothing if status code is higher than 400
        # And return the response text, which usually has 
        # the reson for the failure.
        if response.status_code >= 400:
            logger.error(f"Response TEXT:\n{response.json()}")
            #logger.error(f"Response HEAD:\n{resp_head}")
            return None
        
        # If all is good return the repsonse in JSON
        return response.json()

        #logger.debug(f"Response HEAD: {resp_head}")

        # The response HEAD is allways returned and the JSON response
        # is returned if a response has retuned some text
        #try:
        #    jresp = response.json()
        #    logger.debug(f"Response JSON: {jresp}")
        #except json.decoder.JSONDecodeError as e:
        #    logger.exception(f'Got a JSONDecodeError exception. Check the defined endpoint is correct\n')
        #    logger.exception(f"Response TEXT:\n{response.text}")
        #    logger.exception(f"Response HEAD:\n{resp_head}")
        #    return None, resp_head

        # Return propper values depending on the type of HTTP request 
        # and the response received from it
        #return jresp, resp_head


    def logout(self):
        '''Logs out of the current instance of MM

        Returns
        -------
        The full response in JSON format including `_global_result`

        The error if status string returned is not 0, else it returns None
        '''
        logger.info("Calling logout()")

        url_logout = self._resource_url(uri="/logout")
        resp = self._api_call("POST", url_logout)

        logging.debug(f'Logout response: {resp}')

        # Reset logging to ERROR as this method is called through _api_call and 
        # is not reset as if it were with by calling resource
        logzero.loglevel(logging.ERROR)

        return resp

    def _resource_url(self, **kwargs):
        '''The resource URL formatter
        
        Will return the propperly formated url with any provided org_id, site_id or uri or a
        combination of all

        Args
        ----
        org_id: `str`
            The Organisation ID
        site_id: `str`
            The Site ID
        uri: `str`
            The endpoint resource, e.g. '/self', or 'self', or '/self/'
        
        Returns
        -------
        The full URL string to the requested 'uri' resource under the 'org_id' and 'site_id' if provided.
        '''
        logger.info("Calling _resource_url()")
        logger.info(f"kwargs in: {kwargs}")
        
        url = f"{self.mist_base_api_url}/api/v{self.apiv}/"

        # Set of above parameters that will be skipped by the
        # for loop below so as to not add them again to the URL
        known_id_names = set()

        # List of most used kwargs
        if 'org_id' in kwargs:
            org_id = f'orgs/{kwargs["org_id"]}'
            url = urljoin(url, org_id) + "/"
            known_id_names.add("org_id")
        if 'site_id' in kwargs:
            site_id = f'sites/{kwargs["site_id"]}'
            url = urljoin(url, site_id) + "/"
            known_id_names.add("site_id")
        if 'map_id' in kwargs:
            map_id = f"maps/{kwargs['map_id']}"
            url = urljoin(url, map_id) + "/"
            known_id_names.add("map_id")
        if 'wlan_id' in kwargs:
            wlan_id = f"wlans/{kwargs['wlan_id']}"
            url = urljoin(url, wlan_id) + "/"
            known_id_names.add("wlan_id")
        if 'uri' in kwargs:
            url = urljoin(url, kwargs['uri'].strip('/'))# + "/"
            known_id_names.add("uri")

        # 'params' are special nd are passed to requests as params
        # So to no not be preocessed here, they are put into 
        # known id names
        known_id_names.add("params")

        # Add to URL parameters from kwargs and skip the 
        # ones that are in known_id_names
        for k, v in kwargs.items():
            if k in known_id_names:
                continue
            
            # Constructs the end of the URL from kwargs but
            # skips if a kwargs parameter is not a string
            if isinstance(v, str):
                url = urljoin(f'{url}/', v.lstrip("/"))

        # Remove the last '/' if in the url as it won't work with it
        if url[-1] == "/":
            url = url[:-1]

        logger.debug(f"URL to endpoint: {url}")

        return url

    def _select_cloud(self, cloud):
        '''Cloud selector, which either selects the specified 'cloud' or returns the default 'US' one.

        Params
        ------
        cloud: `str`
            Can be 'us' or 'eu', or 'EU'
        '''
        logger.info("Calling _select_cloud()")

        try:
            return clouds[cloud.upper()]
        except KeyError:
            logging.exception(f'Not a valid entry {list(clouds.keys())}. Using "US" as default.')
            return clouds["US"]


    '''
    def _two_factor_login(self, user_token=None, prev_resp=None):

        if user_token:
            url_2fa = self._resource_url(uri="/api/v1/two_factor")
            resp = self._api_call("POST", url_2fa)
            logger.debug(f'Self data: {resp}')

        if prev_resp and 'two_factor' in prev_resp:
            return
    '''

    def _kwargs_modify(self, data=None, **kwargs):

        logger.info("Calling _kwargs_modify()")
        #logger.debug(f'URI endpoint: {uri}')
        logger.debug(f'Data Payload: {data}')

        #kwargs['uri'] = uri

        # If data is passed in, the HTTP method is POST with that data
        if data:
            kwargs['method'] = 'POST'
        else:
            kwargs['method'] = 'GET'

        logger.debug(f'kwargs out: {kwargs}')

        return kwargs

    def _params(self, **kwargs):

        logger.info("Calling _params()")
        logger.info(f"kwargs in: {kwargs}")

        params = {}

        if 'params' in kwargs:
            params = kwargs['params']

        logger.debug(f"Returned params: {params}")

        return params

    def _determine_method(self, **kwargs):

        logger.info("Calling _determine_method()")

    def resource(self, method, jpayload=None, **kwargs):

        logger.info("Calling resource()")
        logger.debug(f'kwargs in: {kwargs}')
        
        # Get the params from the passed in kwargs
        params = self._params(**kwargs)

        # Build the full URL to the resource
        resource_url = self._resource_url(**kwargs)

        # Get the JSON response and error
        jresp = self._api_call(method, resource_url, params=params, json=jpayload)
        
        # Reset logging to ERROR
        logzero.loglevel(logging.ERROR)

        return jresp

    def whoami(self, method='GET', **kwargs):

        logger.info('Calling whoami()')
        logger.info(f'kwargs in: {kwargs}')


        #kwargs = self._kwargs_modify(f'/api/v{self.apiv}/self', **kwargs)
        kwargs['uri'] = f'/self'

        return self.resource(method, **kwargs)

    def wlans(self, method='GET', data=None, **kwargs):
        #   /api/v1/sites/:site_id/wlans
        #   /api/v1/sites/:site_id/wlans/:wlan_id/
        #   /api/v1/sites/:site_id/wlans/:wlan_id/parameter << POST, DELETE, PUT
        #   /api/v1/sites/:site_id/wlans/derived
        #   /api/v1/sites/:site_id/wlans/derived?resolve=false

        logger.info('Calling wlans()')
        logger.info(f'kwargs in: {kwargs}')

        #kwargs = self._kwargs_modify(**kwargs)
        if not 'wlan_id' in kwargs:
            kwargs['uri'] = f'/wlans'

        return self.resource(method, jpayload=data, **kwargs)



    '''
 

    '''


