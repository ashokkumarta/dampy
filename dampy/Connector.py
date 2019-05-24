# ashokkumar.ta@gmail.com / 24-May-2019

import requests, json
from requests.auth import HTTPBasicAuth
import logging
from dampy.Assets import Assets
from dampy.Response import Response

class Connector:

    cfg = {
        "strict_success": [200, 201],
        "lenient_success": [500],
        "Activate": "/bin/replicate.json",
        "Deactivate": "/bin/replicate.json",
        "Delete": "/bin/wcmcommand"
    }
    MSGS = {
        "service_error": 'Error in service call',
        "non_json_response": 'Not a json in the response',
        "Activate": "/bin/replicate.json",
        "Deactivate": "/bin/replicate.json",
        "Delete": "/bin/wcmcommand"
    }

    def __init__(self, host, user, password):
        self.host = host
        if user:
            self._auth = HTTPBasicAuth(user, password)
        else:
            self._auth = None
        self.dam = Assets(self)

    def rawget(self, path):
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
        
        response = self.rawget(path) 
        try:
            response.jsonify()
        except:
            logging.error(Connector.MSGS['non_json_response'])

        return response

    def post(self, path, data=None, files=None):

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


    def upload(self, asset, path):
        

        try:
            
            # Create DAM folder if not present
            self._check_n_create_folder(path)

            url = self.host + path + '.createasset.html'
            logging.debug('Posting the PDF to the URL - '+ url)
            logging.debug('PDF File : ' + pdf_file)
            files = {'file': open(pdf_file, 'rb')}
            res = requests.post(url, files = files, auth = self._auth)            

            if (self.check(res)):
                logging.info('PDF upload completed successfully')
            else:
                logging.info('PDF upload failed. Invalid reponse received')
        except:
            logging.error('Error in PDF upload')

    def perfrom(self, action, path, name, force='true'):
        

        try:
            url = self.host + Connector.cfg[action]
            full_path =  path + '/' + name
            data = {'cmd': action, 'path':full_path, 'force':force}

            logging.debug(action + '-ing the PDF at - '+ full_path)
            logging.debug('URL - '+ url)
            logging.debug('Data - '+ str(data))

            res = requests.post(url, data = data, auth = self._auth)            

            if (self.check(res)):
                logging.info('PDF '+action+'d successfully')
            else:
                logging.info('PDF '+action+' failed. Invalid reponse received')
        except:
            logging.error('Error in '+action+'-ing PDF')


    def check(self, res, strict=True):
        
        logging.info('Response code : ' + str(res.status_code))
        if res.status_code in Connector.cfg['strict_success']:
            return True
        elif not strict and res.status_code in Connector.cfg['lenient_success']:
            logging.debug('Lenient Success allowed for code : ' + str(res.status_code))
            return True
        else:
            logging.error('Reponse received : \n' + str(res.text))
            return False

