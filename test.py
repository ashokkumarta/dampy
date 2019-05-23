import logging
from PyAEMConnector.AEMConnector import AEMConnector

# Sample usage
if __name__== "__main__":
    # Set logging level
    logging.basicConfig(level=logging.DEBUG)

    # Create a connection
    con = AEMConnector()

    # Fire a get request 
    res = con.get('/content/dam.1.json')

    logging.debug('Res: '+str(res))
