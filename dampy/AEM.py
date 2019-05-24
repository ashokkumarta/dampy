import requests, json
from requests.auth import HTTPBasicAuth
import logging
from dampy.Connector import Connector
from dampy.Assets import Assets

class AEM:

    def __init__(self, host='http://localhost:4502', user='admin', password='admin'):
        conn = Connector(host, user, password)
        self.dam = Assets(conn)

