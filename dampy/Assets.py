# ashokkumar.ta@gmail.com / 24-May-2019

import requests, json
from requests.auth import HTTPBasicAuth
import logging

from dampy.Env import Env
from dampy.Util import *

class Assets:

    CFG = {
        "strict_success": [200, 201],
        "lenient_success": [500],
        'assets_key': 'hits',
        'path_key': 'jcr:path'
    }

    URL = {
        'list': '/bin/querybuilder.json?type=dam:Asset&p.limit=-1&p.hits=selective&p.properties=jcr:path&p.nodedepth=-1&path=',
        'metadata_suffix': '/jcr:content.',
        'metadata_type': '.json',
        "Activate": "/bin/replicate.json",
        "Deactivate": "/bin/replicate.json",
        "deletePage": "/bin/wcmcommand"
    }

    DATA = {
        "CREATE_FOLDER" : "{'./jcr:primaryType': 'sling:OrderedFolder', \
            './jcr:content/jcr:primaryType': 'nt:unstructured', \
            '/jcr:content/jcr:title':'$name', \
            ':name':'$name' }"

    }



    def __init__(self, conn):
        self.conn = conn


    def list(self, path='/content/dam'):
        asset_list = []
        logging.debug(Assets.URL['list'])
        url = Assets.URL['list'] + path
        response = self.conn.get(url)
        if response.success:
            for e in response.data[Assets.CFG['assets_key']]:
                asset_list.append(e[Assets.CFG['path_key']])    
        else:
            logging.error('Error getting the assets list')
            logging.error('Failed due to : '+response.message)
            logging.error('Empty list returned')
        return asset_list

    def metadata(self, asset_path, level=1):
        asset_metadata = {}
        url = asset_path + Assets.URL['metadata_suffix'] + str(level) + Assets.URL['metadata_type']
        response = self.conn.get(url)
        if response.success:
            asset_metadata = response.data
        else:
            logging.error('Error getting the asset metadata')
            logging.error('Failed due to : '+response.message)
            logging.error('Empty metadata returned')
        return asset_metadata


    def _download(self, asset, env, retain_dam_path=True):
        logging.debug("Downloading asset : " + str(asset))
        response = self.conn.rawget(asset)
        env.store(asset, response.data.content, retain_dam_path)
        return True

    def downloadAsset(self, asset, dir='download'):
        env = Env(dir)
        return self._download(asset, env, False)

    def downloadFolder(self, path='/content/dam', dir='download'):
        asset_list = self.list(path)
        logging.debug("Asset list : "+str(asset_list))
        overall_status = True
        if asset_list:
            env = Env(dir)
            for asset in asset_list:
                status = self._download(asset, env)
                overall_status &= status
        return overall_status

    def createFolder(self, path, ignore_error = False):

        parent, name = splitPath(path)
        data = Assets.DATA['CREATE_FOLDER'].replace('$name', name)

        logging.debug('URL - '+ path)
        logging.debug('Data - '+ data)

        response = self.conn.post(path, data = data)            

        if not (ignore_error or response.success):
            logging.error('Error creating folder')
            logging.error('Failed due to : '+response.message)
            logging.error('Check if the folder already exists')
        return response.success

    def uploadAsset(self, file, path='/content/dam'):

        path = trimPath(path)
        
        self.createFolder(path, True)
        
        url = path + '.createasset.html'
        logging.debug('URL - '+ path)
        logging.debug('file - '+ file)

        files = {'file': open(file, 'rb')}
        response = self.conn.post(url, files = files)            
        if not response.success:
            logging.error('Error getting uploading file')
            logging.error('Failed due to : '+response.message)
        return response.success

    def uploadFolder(self, dir='upload'):
       
        env = Env(dir)
        path_map = cleansePaths(dir, env.listFiles() )
        for file in path_map:
            logging.debug('Uploading file - '+ file)
            self.uploadAsset(file, path_map[file])


    def activate(self, path, force='true'):

        url = Assets.URL['Activate']
        data = {'cmd': 'Activate', 'path':path, 'force':force}

        logging.debug('URL - '+ url)
        logging.debug('Data - '+ str(data))

        response = self.conn.post(url, data = data)            

        if not response.success:
            logging.error('Error Activating the asset')
            logging.error('Failed due to : '+response.message)
        return response.success

    def deactivate(self, path, force='true'):

        url = Assets.URL['Deactivate']
        data = {'cmd': 'Deactivate', 'path':path, 'force':force}

        logging.debug('URL - '+ url)
        logging.debug('Data - '+ str(data))

        response = self.conn.post(url, data = data)            

        if not response.success:
            logging.error('Error Deactivating the asset')
            logging.error('Failed due to : '+response.message)
        return response.success


    def delete(self, path, force='true'):

        url = Assets.URL['deletePage']
        data = {'cmd': 'deletePage', 'path':path, 'force':force}

        logging.debug('URL - '+ url)
        logging.debug('Data - '+ str(data))

        response = self.conn.post(url, data = data)            

        if not response.success:
            logging.error('Error Deactivating the asset')
            logging.error('Failed due to : '+response.message)
        return response.success

