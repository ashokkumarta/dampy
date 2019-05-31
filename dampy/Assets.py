# ashokkumar.ta@gmail.com / 24-May-2019

import requests, json
from requests.auth import HTTPBasicAuth
import logging

from dampy.Env import Env
from dampy.Util import *

class Assets:
    '''Class abstracting the DAM operations '''


    CFG = {
        'assets_key': 'hits',
        'path_key': 'jcr:path'
    }

    URL = {
        'list': '/bin/querybuilder.json?type=dam:Asset&p.limit=-1&p.hits=selective&p.properties=jcr:path&p.nodedepth=-1&path=',
        'xprops': '/bin/querybuilder.json?type=dam:Asset&p.limit=-1&p.hits=selective&p.properties=$props&p.nodedepth=-1&path=',
        'uprops': '/content/dam.html',
        'metadata_suffix': '/jcr:content.',
        'metadata_type': '.json',
        'Activate': '/bin/replicate.json',
        'Deactivate': '/bin/replicate.json',
        'deletePage': '/bin/wcmcommand',
        'ActivateTree': '/libs/replication/treeactivation.html'
    }

    DATA = {
        'CREATE_FOLDER' : '{"./jcr:primaryType": "sling:OrderedFolder", \
            "./jcr:content/jcr:primaryType": "nt:unstructured", \
            "/jcr:content/jcr:title":"$title", \
            ":name":"$name" }',
        'U_PROPS' : '{"_charset_": "utf-8", "dam:bulkUpdate": "true", "mode": "hard"}'

    }

    def __init__(self, conn):
        '''
        Initialize an Assets instance with a AEM handle
        '''
        self.conn = conn


    def list(self, path='/content/dam', csv_dump=False, csv_file='output/asset_list.csv'):
        '''
        Get the list of all assets under the path given as parameter and optionally write it to a CSV file
        '''
    
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
        if csv_dump or csv_file:
            logging.debug("Writing asset list of assets to : " + csv_file)
            dir, fname = dir_n_file(csv_file, 'csv')
            env = Env(dir)
            env.writeCSV(fname, list=asset_list)
        return asset_list

    def metadata(self, asset_path, level=1):
        '''
        Get the metadata of the asset. Level specifies for nesting levels for metadata fetch 
        '''
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

    def _metaVal(self, asset, key):
        '''
        Finds the key in the asset json and returns its vale
        '''
        path = key.split('/')
        p_obj = asset
        try:
            for k in path:
                p_obj = p_obj[k]
        except:
            return None
        return p_obj

    def _csvRead(self, csv_file, header=True, type=True):
        '''
        Reads the CSV file and returns the headers, types and data as per the flags passed in
        '''

        headers = []
        types = []
        csv_data = []

        with open(csv_file,'r') as cFile:
            for row in cFile:
                csv_data.append(row.strip().split(","))

        if csv_data and header :
            headers = csv_data.pop(0)
        if csv_data and type :
            types = csv_data.pop(0)
        return headers, types, csv_data

    def xprops(self, path='/content/dam', props=['jcr:path','jcr:content/metadata/dc:title'], csv_file='output/asset_props.csv'):
        '''
        Extracts the metadata properties of the assets under the given path and writes it to an output csv file 
        '''
        asset_data = []
        url = Assets.URL['xprops'] + path
        url = url.replace('$props', ' '.join(props))
        
        logging.debug(url)

        response = self.conn.get(url)
        if response.success:
            asset_data.append(props)
            for asset in response.data[Assets.CFG['assets_key']]:
                asset_props = []
                for key in props:
                    asset_props.append(self._metaVal(asset, key))
                asset_data.append(asset_props)
            logging.debug("Writing asset list of assets to : " + csv_file)
            dir, fname = dir_n_file(csv_file, 'csv')
            env = Env(dir)
            env.writeCSV(fname, data=asset_data)
            return True
        else:
            logging.error('Error extracting asset properties')
            logging.error('Failed due to : '+response.message)
            logging.error('Empty list returned')
        return False

    def uprops(self, csv_file='input/asset_props.csv'):
        '''
        Reads a CSV file and updates the asset perperties based on this CSV data 
        '''
        headers, types, csv_data = self._csvRead(csv_file)
        if not headers:
            logging.error('Invalid CSV input file')
            logging.error('First row of CSV must be headers')
            return False
        elif ( "jcr:path" != headers[0]):
            logging.error('Invalid CSV input file')
            logging.error('The first column of header must be jcr:path property')
            return False
        if not types:
            logging.error('Invalid CSV input file')
            logging.error('Second row of CSV must be types')
            return False

        overall_status = True
        for row in csv_data:

            api_a_path = row[0][12:]
            update_properties = json.loads(Assets.DATA['U_PROPS'])

            for index, header in enumerate(headers):
                if index > 0 and header:
                    update_properties['.' + api_a_path + '/' + header] = row[index]
                    update_properties['.' + api_a_path + '/' + header + '@TypeHint'] = types[index]
            
            logging.debug('Updating with : ',json.dumps(update_properties))
            response = self.conn.post(Assets.URL['uprops'], data = update_properties)
            if not response.success :
                logging.error('Error updating properties for asset : ',update_properties)
                overall_status = False
        return overall_status


    def _download(self, asset_path, env, retain_dam_path):
        '''
        Downlods the asset to the directory represented by the env object
        '''
        logging.debug("Downloading asset : " + str(asset_path))
        response = self.conn.rawget(asset_path)
        env.store(asset_path, response.data.content, retain_dam_path)
        return True

    def downloadAsset(self, asset_path, dir='download', retain_dam_path=False):
        '''
        Downlods the asset to the dir
        '''
        env = Env(dir)
        return self._download(asset_path, env, retain_dam_path)

    def downloadFolder(self, path='/content/dam', dir='download', retain_dam_path=True):
        '''
        Downlods all assets under the mentioned DAM path to the dir
        '''
        asset_list = self.list(path)
        logging.debug("Asset list : "+str(asset_list))
        overall_status = True
        if asset_list:
            env = Env(dir)
            for asset in asset_list:
                status = self._download(asset, env, retain_dam_path)
                overall_status &= status
        return overall_status

    def createFolder(self, path, title=None, ignore_error = False):
        '''
        Creates the folder specified by the path in DAM
        '''

        parent, name = splitPath(path)
        data = Assets.DATA['CREATE_FOLDER'].replace('$name', name)
        if title:
            data = Assets.DATA['CREATE_FOLDER'].replace('$title', title)
        else:
            data = Assets.DATA['CREATE_FOLDER'].replace('$title', name)

        logging.debug('URL - '+ path)
        logging.debug('Data - '+ data)

        response = self.conn.post(path, data = data)            

        if not (ignore_error or response.success):
            logging.error('Error creating folder')
            logging.error('Failed due to : '+response.message)
            logging.error('Check if the folder already exists')
        return response.success

    def uploadAsset(self, file, path='/content/dam'):
        '''
        Uploads the single file to DAM at the specified path
        '''

        path = trimPath(path)
        
        self.createFolder(path, None, True)
        
        url = path + '.createasset.html'
        logging.debug('URL - '+ path)
        logging.debug('file - '+ file)

        files = {'file': open(file, 'rb')}
        response = self.conn.post(url, files = files)            
        if not response.success:
            logging.error('Error getting uploading file')
            logging.error('Failed due to : '+response.message)
        return response.success

    def uploadFolder(self, dir='upload', path='/content/dam'):
        '''
        Upload all the assets under the dir parameter. 
        Folder structure under dir replicated onto DAM, under the path specified
        '''
       
        env = Env(dir)
        path_map = cleansePaths(dir, env.listFiles(), path )
        overall_status = True
        for file in path_map:
            logging.debug('Uploading file - '+ file)
            status = self.uploadAsset(file, path_map[file])
            overall_status &= status
        return overall_status

    def activate(self, path, force='true'):
        '''
        Activate the asset or folder specified by the path parameter
        '''

        metadata = self.metadata(path)

        if('dam:AssetContent' == metadata['jcr:primaryType']) :
            url = Assets.URL['Activate']
        else :
            url = Assets.URL['ActivateTree']

        data = {'cmd': 'Activate', 'path':path, 'force':force}

        logging.debug('URL - '+ url)
        logging.debug('Data - '+ str(data))

        response = self.conn.post(url, data = data)            

        if not response.success:
            logging.error('Error Activating the asset')
            logging.error('Failed due to : '+response.message)
        return response.success

    def deactivate(self, path, force='true'):
        '''
        Deactivate the asset or folder specified by the path parameter
        '''

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
        '''
        Delete the asset or folder specified by the path parameter
        '''

        url = Assets.URL['deletePage']
        data = {'cmd': 'deletePage', 'path':path, 'force':force}

        logging.debug('URL - '+ url)
        logging.debug('Data - '+ str(data))

        response = self.conn.post(url, data = data)            

        if not response.success:
            logging.error('Error Deactivating the asset')
            logging.error('Failed due to : '+response.message)
        return response.success

