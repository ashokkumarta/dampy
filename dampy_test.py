import logging
import json

from dampy import AEM

# Sample usage
if __name__== "__main__":

    ## Create an AEM handle. Connects by default to localhost:4502 with admin/admin
    aem = AEM()

    # List all assets under a path
    print ('List all assets under a path')
    list = aem.dam.list('/content/dam/we-retail/en/products/apparel/shorts')
    for asset in list:
        print (asset)

    # Get Metadata of an asset
    print ('Get Metadata of an asset')
    metadata = aem.dam.metadata('/content/dam/we-retail/en/products/apparel/shorts/Bahamas.jpg')
    print(json.dumps(metadata))

    # Download an asset to a local folder. By default gets downloaded to a folder named 'download'
    print ('Download an asset to a local folder')
    status = aem.dam.downloadAsset('/content/dam/we-retail/en/products/apparel/shorts/Bahamas.jpg')
    print('Status : '+str(status))
    
    # Download all assets under a path. By default assets tree get downloaded under a folder named 'download'
    print ('Download all assets under a path')
    status = aem.dam.downloadFolder('/content/dam/we-retail/en/products/apparel/shorts')
    print('Status : '+str(status))

    # Create the new folder 
    print ('Create the new folder')
    status = aem.dam.createFolder('/content/dam/dampy/samples')
    print('Status : '+str(status))

    # Upload an asset at the specified path. Uploads under /content/dam if path not specified 
    print ('Upload an asset at the specified path')
    status = aem.dam.uploadAsset('upload/Shorts_men.jpg', '/content/dam/dampy/samples')
    print('Status : '+str(status))

    # Upload all assets in a local folder to DAM. By default uploads all assets under the folder named 'upload' 
    print ('Upload all assets in a local folder to DAM')
    status = aem.dam.uploadFolder()
    print('Status : '+str(status))

    # Activate an asset
    print ('Activate an asset')
    status = aem.dam.activate('/content/dam/dampy/samples/Shorts_men.jpg')
    print('Status : '+str(status))

    # Deactivate an asset
    print ('Deactivate an asset')
    status = aem.dam.deactivate('/content/dam/dampy/samples/Shorts_men.jpg')
    print('Status : '+str(status))

    # Delete an asset
    print ('Delete an asset')
    status = aem.dam.delete('/content/dam/dampy/samples/Shorts_men.jpg')
    print('Status : '+str(status))

