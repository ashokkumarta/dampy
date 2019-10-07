# ashokkumar.ta@gmail.com / 24-May-2019

import os
import logging
import csv

class Env:
    '''
    Provides a handle to work with the local file system
    Initialized with a directory which is the base under which reads and writes can be performed
    '''

    def __init__(self, dir):
        '''
        Initialize an Env instance with a directory
        '''
        if not dir:
            self.dir = '.'
        self.dir = str(dir)
    
    def _ensure(self, asset, retain_dam_path=True):
        '''
        Checks and creates the folders needed under the env directory to store an asset
        and returns the full path reference for an asset
        '''

        logging.debug("Dir : "+str(self.dir))
        logging.debug("asset : "+str(asset))
        logging.debug("asset : "+str(asset))
        if retain_dam_path:
            full_path = self.dir + asset
            dir_path = os.path.dirname(full_path)
        else:
            full_path = self.dir + '/' + os.path.basename(asset)
            dir_path = os.path.dirname(full_path)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        return full_path

    def store(self, asset, content, retain_dam_path=True):
        '''
        Stores the asset under the directory represented by this env
        '''
        full_path = self._ensure(asset, retain_dam_path)
        f_out = open(full_path, 'wb')
        f_out.write(content)
        f_out.close()

    def listFiles(self):
        '''
        Returns list of all the files present under the directory represented by this env
        '''

        files = []
        for r, d, f in os.walk(self.dir):
            for file in f:
                files.append(os.path.join(r, file).replace("\\","/"))
        return files

    def listDirs(self):
        '''
        Returns list of all the files present under the directory represented by this env
        '''

        dirs = []
        for r, d, f in os.walk(self.dir):
            for dir in d:
                dirs.append(os.path.join(r, dir).replace("\\","/"))
        return dirs

    def writeCSV(self, fname, list=None, data=None):
        '''
        Writes the data to the file under the directory represented by this env
        '''
        full_path = self._ensure(fname, False)
        with open(full_path, 'w', newline='') as csvout:
            wr = csv.writer(csvout, dialect='excel')
            if list:
                for v in list:
                    wr.writerow([v])
            elif data:
                for v in data:
                    wr.writerow(v)
