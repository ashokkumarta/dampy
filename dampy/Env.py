import os
import logging

class Env:
    def __init__(self, dir):
        if not dir:
            self.dir = '.'
        self.dir = str(dir)
    
    def _ensure(self, asset, retain_dam_path=True):
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
        full_path = self._ensure(asset, retain_dam_path)
        f_out = open(full_path, 'wb')
        f_out.write(content)
        f_out.close()

    def listFiles(self):
        files = []
        for r, d, f in os.walk(self.dir):
            for file in f:
                files.append(os.path.join(r, file).replace("\\","/"))
        return files

