# ashokkumar.ta@gmail.com / 24-May-2019

import requests, json
from requests.auth import HTTPBasicAuth
import logging
import csv, ast
import hashlib

from dampy.lib.Config import *
from dampy.lib.Util import *
from dampy.lib.Env import Env


class Assets:
    '''Class abstracting the DAM operations '''

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
        url = urls['list'] + path

        logging.debug('URL : '+url)

        response = self.conn.get(url)

        if response.success:
            for e in response.data[keys.assets_key]:
                asset_list.append(e[keys.path_key])    
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
        url = asset_path + urls['metadata_suffix'] + str(level) + urls['metadata_type']
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
            csv_reader = csv.reader(cFile, delimiter=',')
            for row in csv_reader:
                csv_data.append(row)

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
        url = urls['xprops'] + path
        url = url.replace('$props', ' '.join(props))
        
        logging.debug(url)

        response = self.conn.get(url)
        if response.success:
            asset_data.append(props)
            for asset in response.data[keys.assets_key]:
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
            update_properties = ast.literal_eval(msgs['uprops'])

            for index, header in enumerate(headers):
                if index > 0 and header:
                    if '[]' in types[index]:
                        vals = ast.literal_eval(row[index])
                        for v in vals:
                            update_properties.append(('.' + api_a_path + '/' + header, v))
                    else:
                        update_properties.append(('.' + api_a_path + '/' + header, row[index]))

                    update_properties.append(('.' + api_a_path + '/' + header + '@TypeHint', types[index]))
            
            logging.debug('Updating with : ' + json.dumps(update_properties))
            response = self.conn.post(urls['uprops'], data = update_properties)
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
        n_name=namify(name)
        n_path=namify(path)

        data = msgs['createFolder'].replace('$name', n_name)
        if title:
            data = data.replace('$title', title)
        else:
            data = data.replace('$title', name)

        data = json.loads(data)

        logging.debug('URL - '+ n_path)
        logging.debug('Data - '+ str(data))

        response = self.conn.post(n_path, data = data)            

        if not (ignore_error or response.success):
            logging.error('Error creating folder')
            logging.error('Failed due to : '+response.message)
            logging.error('Check if the folder already exists')
        return response.success

    def createFolderTree(self,  path='/content/dam', srcDir=None, srcList=None, ignore_error = False):
        '''
        Creates the folder tree structure in DAM under the given path, reflecting the structure in local dir 
        '''
        dirList = []

        if srcList:
            if isinstance(srcList, list):
               dirList += cleanseDirList('', srcList, path )
            elif isinstance(srcList, str):
                headers, types, csv_data = self._csvRead(srcList, False, False)
                for row in csv_data:
                    dirList += cleanseDirList('', row, path )
            else:
                logging.error('Invalid input for srcList')

        if srcDir:
            env = Env(srcDir)
            dirList += cleanseDirList(srcDir, env.listDirs(), path )

        logging.debug('Creating Folders for - '+ str(dirList))
        overall_status = True
        for dir in dirList:
            logging.debug('Creating Folder - '+ dir)
            status = self.createFolder(dir)
            overall_status &= status
        return overall_status

    def fetchFolderTree(self, path='/content/dam', csv_file='output/folder_tree.csv', props=['jcr:path', 'jcr:content/jcr:title']):
        '''
        Fetches the folder structure under the given path and writes it to an output csv file 
        '''
        folder_data = []
        url = urls['fetchFolderTree'] + path
        url = url.replace('$props', ' '.join(props))
        
        logging.debug(url)

        response = self.conn.get(url)
        if response.success:
            folder_data.append(props)
            for folder in response.data[keys.assets_key]:
                folder_props = []
                for key in props:
                    folder_props.append(self._metaVal(folder, key))
                folder_data.append(folder_props)
            logging.debug("Writing folder list to : " + csv_file)
            dir, fname = dir_n_file(csv_file, 'csv')
            env = Env(dir)
            env.writeCSV(fname, data=folder_data)
        else:
            logging.error('Error fetching folder list')
            logging.error('Failed due to : '+response.message)
            logging.error('Empty list returned')
        return folder_data


    def updateFolderTitle(self, path, newTitle):
        '''
        Updates the folder title with the new value provided
        '''

        url = urls['updateFolderTitle']
        data = json.loads(msgs['updateFolderTitle'].replace('$path', path).replace('$title',newTitle))

        logging.debug('URL - '+ url)
        logging.debug('Data - '+ str(data))

        response = self.conn.post(url, data = data)            

        if not response.success:
            logging.error('Error updating folder title')
            logging.error('Failed due to : '+response.message)
        return response.success

    def restructure(self, inputCSV='input/restructure.csv'):
        '''
        Restructures the DAM folder structure based on the input CSV file 
        '''

        headers, types, csv_data = self._csvRead(inputCSV, True, False)

        overall_status = True
        for row in csv_data:
            logging.debug('Processing row - '+ str(row))
            if('Move' == row[0]):
                srcPath = row[1]
                destPath = row[3]
                dparent, dname = splitPath(destPath)
                status = self.move(srcPath, dparent, dname)
                if(row[1] != row[4]):
                    self.updateFolderTitle(destPath,row[4])
            elif ('Delete' == row[0]):
                status = self.delete(row[1])
            overall_status &= status
        return overall_status


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


    def move(self, srcPath, destPath, newName=None):
        '''
        Move the asset or folder from the srcPath to the destPath
        '''

        url = urls['move']
        data = msgs['move'].replace('$srcPath', srcPath).replace('$destParentPath',destPath)
        if newName:
            data = data.replace('$destName', newName)
        else:
            parent, name = splitPath(srcPath)
            data = data.replace('$destName', name)

        data = json.loads(data)

        logging.debug('URL - '+ url)
        logging.debug('Data - '+ str(data))

        response = self.conn.post(url, data = data)            

        if not response.success:
            logging.error('Error moving ' + srcPath + ' to ' + destPath)
            logging.error('Failed due to : '+response.message)
        return response.success


    def activate(self, path, force='true'):
        '''
        Activate the asset or folder specified by the path parameter
        '''

        metadata = self.metadata(path)

        if('dam:AssetContent' == metadata['jcr:primaryType']) :
            url = urls['activate']
        else :
            url = urls['activateTree']

        data = json.loads(msgs['activate'].replace('$path', path))

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

        url = urls['deactivate']
        data = json.loads(msgs['deactivate'].replace('$path', path))

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

        url = urls['delete']
        data = json.loads(msgs['delete'].replace('$path', path))

        logging.debug('URL - '+ url)
        logging.debug('Data - '+ str(data))

        response = self.conn.post(url, data = data)            

        if not response.success:
            logging.error('Error Deactivating the asset')
            logging.error('Failed due to : '+response.message)
        return response.success

    def activateList(self, listSrc):
        '''
        Activate all the assets provided by the listSrc.
        listSrc can be a list of all assets to activate or the file name containing the list of assets
        '''

        return self._perform(self.activate, listSrc)

    def deactivateList(self, listSrc):
        '''
        Deactivate all the assets provided by the listSrc.
        listSrc can be a list of all assets to deactivate or the file name containing the list of assets
        '''

        return self._perform(self.deactivate, listSrc)

    def deleteList(self, listSrc):
        '''
        Delete all the assets provided by the listSrc.
        listSrc can be a list of all assets to delete or the file name containing the list of assets
        '''

        return self._perform(self.delete, listSrc)


    def _perform(self,  action, listSrc):
        '''
        Creates the folder tree structure in DAM under the given path, reflecting the structure in local dir 
        '''
        assetList = []

        if listSrc:
            if isinstance(listSrc, list):
               assetList += cleanseDirList('', listSrc, '/content/dam' )
            elif isinstance(listSrc, str):
                headers, types, csv_data = self._csvRead(listSrc, False, False)
                logging.debug('Asset list from ' + listSrc + ' - '+ str(csv_data))
                for row in csv_data:
                    assetList += cleanseDirList('', row, '/content/dam' )
            else:
                logging.error('Invalid input for listSrc')

        logging.debug('Performing '+ str(action) +' for - '+ str(assetList))
        overall_status = True
        for asset in assetList:
            logging.debug('Processing asset - '+ asset)
            overall_status &= action(asset)
        return overall_status

    def exists(self, asset):
        '''
        Check if the file is available in DAM and returns the list of paths at which the file is available 
        '''

        fcontent = open(asset, 'rb').read()
        _sha1 = hashlib.sha1(fcontent).hexdigest()

        url = urls['exists'] + _sha1

        logging.debug('URL - '+ url)

        response = self.conn.get(url)

        duplicates = []

        if response.success:
            for e in response.data[keys.assets_key]:
                duplicates.append(e[keys.path_key])    
        else:
            logging.error('Error checking if the given asset exists in DAM')
            logging.error('Failed due to : '+response.message)
            logging.error('Empty list returned')

        return duplicates

    def duplicates(self, path='/content/dam'):
        '''
        Find all the duplicate binaries under the given path and returns it. Returns empty if no duplicates are identified 
        '''

        url = urls['duplicates'] + path

        logging.debug('URL - '+ url)

        response = self.conn.get(url)

        duplicates = {}
        removals = []

        if response.success:
            for e in response.data[keys.assets_key]:
                sha_val = self._metaVal(e, keys.sha1_key)
                if sha_val in duplicates:
                    duplicates[sha_val].append(e[keys.path_key])
                else:
                    duplicates[sha_val] = [e[keys.path_key]]
            for k in duplicates:
                if len(duplicates[k]) <=1:
                    removals.append(k)
            for k in removals:
                duplicates.pop(k)
        else:
            logging.error('Error checking for duplicates in DAM')
            logging.error('Failed due to : '+response.message)
            logging.error('Empty list returned')

        return duplicates

    def checkout(self, path, action='checkout'):
        '''
        Check-out/check-in an asset in DAM
        '''

        url =  path + urls['checkout']
        data = json.loads(msgs[action])

        logging.debug('URL - '+ url)
        logging.debug('Data - '+ str(data))
        print('URL - '+ url)
        print('Data - '+ str(data))

        response = self.conn.post(url, data = data)            

        if not (response.success):
            print('Error checking out the asset')
            logging.error('Error checking out the asset')
            logging.error('Failed due to : '+response.message)
            logging.error('Check if the asset exists and is not locked')
        return response.success

    def checkin(self, path):
        '''
        Check-in an asset in DAM. Calls checkout method with action param as 'checkin' to 
        accomplish the task
        '''
        return self.checkout(path, action='checkin')

