import os, json
import logging

class _Config:

    def _load(self):
        'Loads the config file and returns json object'
        config_file = 'config/config.json'
        logging.debug('Checking configuration file...')
        try: 
            config_file = os.environ['CONFIG_FILE']
        except:
            logging.debug('Config file path not defined. Loading the default config file')
        
        config=open(config_file).read()
        logging.debug('configuration parameters:\n'+config)
        self._config_json = json.loads(config)

    def __getitem__(self, key):
        if self._mode:
            return self._config_json[self._mode][key]
        return self._config_json[key]

    def __getattr__(self, attr):
        return self.__getitem__(attr)

    def __init__(self, mode=None):
        logging.debug('Loading the configuration')
        self._load()
        self._mode = mode

keys = _Config('keys')
urls = _Config('urls')
msgs = _Config('msgs')
