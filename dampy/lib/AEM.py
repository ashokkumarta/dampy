# ashokkumar.ta@gmail.com / 24-May-2019

import requests, json
from requests.auth import HTTPBasicAuth
import logging

from dampy.lib.Connector import Connector
from dampy.lib.Assets import Assets

class AEM:
    '''Class abstracting an AEM instance '''

    def __init__(self, host='http://localhost:4502', user='admin', password='admin'):
        '''
        Create an AEM instance
        >>> AEM() # Creates a handle to AEM instance connecting to http://localhost:4502 with credentials admin/admin

        >>> AEM('http://my_aem_host:port') # Creates a handle to AEM instance connecting to http://my_aem_host:port with credentials admin/admin

        >>> AEM('http://my_aem_host:port', 'userid', 'password') # Creates a handle to AEM instance connecting to http://my_aem_host:port with given credentials 

        '''
        conn = Connector(host, user, password)
        self.dam = Assets(conn)

