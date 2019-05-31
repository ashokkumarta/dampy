# ashokkumar.ta@gmail.com / 24-May-2019

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

    # List all assets under a path and wirte it to default CSV file
    print ('List all assets under a path and wirte it to default CSV file')
    list = aem.dam.list('/content/dam/we-retail', True)
    for asset in list:
        print (asset)

    # List all assets under a path and wite it to teh CSV file specified
    print ('List all assets under a path and wite it to teh CSV file specified')
    list = aem.dam.list('/content/dam/we-retail/en/products', True, 'output/all_products.csv')
    for asset in list:
        print (asset)

    # Create the new folder 
    print ('Create the new folder')
    status = aem.dam.createFolder('/content/dam/dampy/test/samples')
    print('Status : '+str(status))

    # Create the new folder, specifying a title 
    print ('Create the new folder, specifying a title')
    status = aem.dam.createFolder('/content/dam/dampy/test/new_samples', 'My New Sample')
    print('Status : '+str(status))

    # Upload an asset. Uploads under /content/dam as path is not specified 
    print ('Upload an asset at the specified path')
    status = aem.dam.uploadAsset('upload/Shorts_men.jpg')
    print('Status : '+str(status))

    # Upload an asset at the specified path - dampy/test/samples. 
    print ('Upload an asset at the specified path')
    status = aem.dam.uploadAsset('upload/Shorts_men.jpg', '/content/dam/dampy/test/samples')
    print('Status : '+str(status))

    # Upload all assets in a local upload folder to DAM under dampy/test/new_samples. By default uploads all assets from the folder named 'upload' 
    print ('Upload all assets in a local folder to DAM')
    status = aem.dam.uploadFolder(path='/content/dam/dampy/test/new_samples')
    print('Status : '+str(status))

    # Upload all assets in a local folder 'upload_test' to DAM under dampy/test/samples.  
    print ('Upload all assets in a local folder to DAM at the specified path')
    status = aem.dam.uploadFolder(dir='upload/products', path='/content/dam/dampy/test/samples')
    print('Status : '+str(status))

    # Download an asset to a local folder. By default gets downloaded to a folder named 'download'
    print ('Download an asset to a local folder')
    status = aem.dam.downloadAsset('/content/dam/dampy/test/samples/Shorts_men.jpg')
    print('Status : '+str(status))
    
    # Download an asset to a local folder, retaining the DAM path in local. By default gets downloaded to a folder named 'download'
    print ('Download an asset to a local folder, retaining the DAM path in local')
    status = aem.dam.downloadAsset('/content/dam/dampy/test/samples/Shorts_men.jpg', retain_dam_path=True)
    print('Status : '+str(status))

    # Download all assets under a path. By default assets tree get downloaded under a folder named 'download'
    print ('Download all assets under a path')
    status = aem.dam.downloadFolder('/content/dam/dampy/test/samples')
    print('Status : '+str(status))

    # Download all assets under a DAM path to local, ignoring the DAM folder tree hierarchy. By default assets tree get downloaded under a folder named 'download'
    print ('Download all assets under a DAM path to local, ignoring the DAM folder tree hierarchy')
    status = aem.dam.downloadFolder('/content/dam/dampy/test/new_samples', 'download/test', False)
    print('Status : '+str(status))

    # Get Metadata of an asset
    print ('Get Metadata of an asset')
    metadata = aem.dam.metadata('/content/dam/dampy/test/samples/Shorts_men.jpg')
    print(metadata)

    # Extract default properties of assets under the given path and write it to a CSV file
    print ('Extract properties of assets under the given path and write it to a CSV file')
    status = aem.dam.xprops('/content/dam/dampy/test/samples')
    print('Status : '+str(status))

    # Extract specific properties of assets under the given path and write it to a CSV file
    print ('Extract specific properties of assets under the given path and write it to a CSV file')
    status = aem.dam.xprops('/content/dam/dampy/test', ['jcr:path', 'jcr:content/metadata/dc:title','jcr:content/metadata/jcr:title'])
    print('Status : '+str(status))

    # Update properties of assets based on an input CSV file
    print ('Update properties of assets based on an input CSV file')
    status = aem.dam.uprops()
    print('Status : '+str(status))

    # Update properties of assets based on an input CSV file
    print ('Update properties of assets based on an input CSV file')
    status = aem.dam.uprops('input/my_asset_update.csv')
    print('Status : '+str(status))

    # Extract specific properties of assets under the given path and write it to a CSV file
    print ('Extract specific properties of assets under the given path and write it to a CSV file')
    status = aem.dam.xprops('/content/dam/dampy/test', ['jcr:path', 'jcr:content/metadata/dc:title','jcr:content/metadata/jcr:title'], 'output/after_my_update.csv')
    print('Status : '+str(status))

    # Activate an asset
    print ('Activate an asset')
    status = aem.dam.activate('/content/dam/dampy/test/samples/Shorts_men.jpg')
    print('Status : '+str(status))

    # Activate a folder
    print ('Activate an asset')
    status = aem.dam.activate('/content/dam/dampy/test/samples')
    print('Status : '+str(status))

    # Deactivate an asset
    print ('Deactivate an asset')
    status = aem.dam.deactivate('/content/dam/dampy/test/samples/Shorts_men.jpg')
    print('Status : '+str(status))

    # Deactivate an asset
    print ('Deactivate a folder')
    status = aem.dam.deactivate('/content/dam/dampy/test/samples')
    print('Status : '+str(status))

    # Delete an asset
    print ('Delete an asset')
    status = aem.dam.delete('/content/dam/Shorts_men.jpg')
    print('Status : '+str(status))

    # Delete an asset
    print ('Delete a folder')
    status = aem.dam.delete('/content/dam/dampy/test')
    print('Status : '+str(status))
