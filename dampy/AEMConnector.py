import requests, json
from requests.auth import HTTPBasicAuth
import logging

class AEMConnector:

    cfg = {
        "strict_success": [200, 201],
        "lenient_success": [500],
        "Activate": "/bin/replicate.json",
        "Deactivate": "/bin/replicate.json",
        "Delete": "/bin/wcmcommand"
    }

    def __init__(self, host='http://localhost:4502', user='admin', password='admin'):
        self.host = host
        if user:
            self._auth = HTTPBasicAuth(user, password)
        else:
            self._auth = None

    def get(self, path):
        
        try:
            logging.debug('Forming the URL')
            url = self.host + path
            logging.debug('Forming the URL - '+ url)

            logging.debug('Fetching response from the URL')
            res = requests.get(url, auth=self._auth) 
            if( self.check(res)):
                res_json = res.json()
                return res_json
        except:
            logging.error('Error in service call')
        return {}

    def _check_n_create_folder(self, path):

        logging.debug('Trying to create folders for the path : '+path)
        parent, name = get_asset(path)

        try:
            url = self.host + parent + '/'
            data = {'./jcr:primaryType': 'sling:OrderedFolder', 
                './jcr:content/jcr:primaryType': 'nt:unstructured', 
                '/jcr:content/jcr:title':name, \
                ':name':name, }

            logging.debug('URL - '+ url)
            logging.debug('Data - '+ str(data))

            res = requests.post(url, data = data, auth = self._auth)            

            if (self.check(res, False)):
                logging.info('Path '+path+' checked and created successfully')
            else:
                logging.info('Path '+path+' creation failed. Path may exist already... Proceeding')
        except:
            logging.error('Error in creating path '+path)

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
            url = self.host + AEMConnector.cfg[action]
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
        
        logging.debug('Response code : ' + str(res.status_code))
        if res.status_code in AEMConnector.cfg['strict_success']:
            return True
        elif not strict and res.status_code in AEMConnector.cfg['lenient_success']:
            logging.debug('Lenient Success allowed for code : ' + str(res.status_code))
            return True
        else:
            logging.debug('Reponse received : \n' + str(res.text))
            logging.debug('...............................\n')
            return False

