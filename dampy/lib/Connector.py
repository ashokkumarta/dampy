# ashokkumar.ta@gmail.com / 24-May-2019

import requests, json
from requests.auth import HTTPBasicAuth
import logging

from dampy.lib.Assets import Assets
from dampy.lib.Response import Response

class Connector:
    '''
    Connects to and performs the get and post operations on the connected AEM instance
    '''    

    CFG = {
        "strict_success": [200, 201],
        "lenient_success": [500]
    }

    MSGS = {
        "service_error": 'Error in service call',
        "non_json_response": 'Not a json in the response'
    }

    def __init__(self, host, user, password):
        '''
        Initialize connection to the host with given user and password
        '''
        self.host = host
        if user:
            self._auth = HTTPBasicAuth(user, password)
        else:
            self._auth = None
        self.dam = Assets(self)

    def rawget(self, path):
        '''
        Performs a get operation to the path and returns the raw response as-is
        '''
        try:
            url = self.host + path
            logging.debug('URL - '+ url)
            result = requests.get(url, auth=self._auth) 
            logging.debug('Response from the URL : '+str(result))
            if( self.check(result)):
                return Response(True, None, result)
        except:
            logging.error(Connector.MSGS['service_error'])
            return Response(False, Connector.MSGS['service_error'], None)

        return Response(False, str(result.status_code) + '/' + result.text, None)


    def get(self, path):
        '''
        Performs a get operation to the path, converts the response data to json and returns it
        '''
        
        response = self.rawget(path) 
        try:
            response.jsonify()
        except:
            logging.error(Connector.MSGS['non_json_response'])

        return response

    def post(self, path, data=None, files=None):
        '''
        Performs a post operation to the path, sending the data and files parameters
        '''

        logging.debug('Performing post to ' + path)
        try:
            url = self.host + path 

            logging.debug('URL - '+ url)

            result = requests.post(url, data = data, files = files, auth = self._auth)            

            if (self.check(result, False)):
                return Response(True, None, result)
        except:
            logging.error(Connector.MSGS['service_error'])
            return Response(False, Connector.MSGS['service_error'], None)

        return Response(False, str(result.status_code) + '/' + result.text, None)


    def check(self, res, strict=True):
        '''
        Checks the status of the response and returns
        True on successful response
        False on error response  
        '''
        
        logging.info('Response code : ' + str(res.status_code))
        if res.status_code in Connector.CFG['strict_success']:
            return True
        elif not strict and res.status_code in Connector.CFG['lenient_success']:
            logging.debug('Lenient Success allowed for code : ' + str(res.status_code))
            return True
        else:
            logging.error('Reponse received : \n' + str(res.text))
            return False

