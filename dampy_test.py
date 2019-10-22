# ashokkumar.ta@gmail.com / 24-May-2019

from dampy import AEM

# Sample usage
if __name__== "__main__":

    #Enable logging
    import logging
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    ## Create an AEM handle. Connects by default to localhost:4502 with admin/admin
    aem = AEM("http://localhost:4502")

    # List all assets under a path
    logging.debug ('List all assets under a path')
    list = aem.dam.list('/content/dam/we-retail/en/products/apparel/shorts')
    for asset in list:
        logging.debug (asset)

    # List all assets under a path and wirte it to default CSV file
    logging.debug ('List all assets under a path and wirte it to default CSV file')
    list = aem.dam.list('/content/dam/we-retail', True)
    for asset in list:
        logging.debug (asset)

    # List all assets under a path and wite it to the CSV file specified
    logging.debug ('List all assets under a path and wite it to the CSV file specified')
    list = aem.dam.list('/content/dam/we-retail/en/products', True, 'output/all_products.csv')
    for asset in list:
        logging.debug (asset)

    # Create the new folder 
    logging.debug ('Create the new folder')
    status = aem.dam.createFolder('/content/dam/dampy/test/samples')
    logging.debug('Status : '+str(status))

    # Create the new folder, specifying a title 
    logging.debug ('Create the new folder, specifying a title')
    status = aem.dam.createFolder('/content/dam/dampy/test/new_samples', 'My New Sample')
    logging.debug('Status : '+str(status))

    # Create the folder tree structure in DAM 
    logging.debug ('Create folder tree, based on local folder structure under the path /content/dam/dampy/test')
    status = aem.dam.createFolderTree(path='/content/dam/dampy/test', srcDir='upload/Folder Tree Dir')
    logging.debug('Status : '+str(status))


    # Create the folder tree structure in DAM 
    logging.debug ('Create folder tree, based on entries in input text file')
    status = aem.dam.createFolderTree( srcList='input/flist.txt')
    logging.debug('Status : '+str(status))

    # Create the folder tree structure in DAM 
    logging.debug ('Create folder tree, based on entries in input CSV file')
    status = aem.dam.createFolderTree(srcList='input/Folder_tree.csv')
    logging.debug('Status : '+str(status))

    # Create the folder tree structure in DAM 
    logging.debug ('Create folder tree, based on input provided as a list')
    status = aem.dam.createFolderTree(srcList=['/content/dam/dampy/test/Folder Tree LIST', '/content/dam/dampy/test/Folder Tree LIST/New EVENT'])
    logging.debug('Status : '+str(status))

    # Update the title of the folder to the new value provided 
    logging.debug ('Update the title of the folder to the new value provided')
    status = aem.dam.updateFolderTitle(path='dampy/test/folder-tree-txt', newTitle='Root Folder from Text tree')
    logging.debug('Status : '+str(status))

    # Move the folder from the source path to the destination path  
    logging.debug ('Move the folder from the source path to the destination path')
    status = aem.dam.move(srcPath='/content/dam/dampy/test/folder-tree-txt', destPath='/content/dam/dampy/test/folder-tree-list')
    logging.debug('Status : '+str(status))

    # Move the folder from the source path to the destination path with a new name 
    logging.debug ('Move the folder from the source path to the destination path with a new name')
    status = aem.dam.move(srcPath='/content/dam/dampy/test/folder-tree-list/folder-tree-txt', destPath='/content/dam/dampy/test/folder-tree-list', newName='text-tree')
    logging.debug('Status : '+str(status))

    # Fetch the folder tree structure from DAM and write it to the default CSV file 
    logging.debug ('Fetch the folder tree structure from DAM and write it to CSV file ')
    status = aem.dam.fetchFolderTree(path='/content/dam/dampy/test')
    logging.debug('Status : '+str(status))

    # Restructure the folders in DAM, moving and deleting folders and updating folder title based on input CSV file 
    logging.debug ('Restructure the folders in DAM, moving and deleting folders and updating folder title based on input CSV file')
    status = aem.dam.restructure(inputCSV='input/restructure.csv')
    logging.debug('Status : '+str(status))

    # Fetch the folder tree structure from DAM and write it to the specified CSV file 
    logging.debug ('Fetch the folder tree structure from DAM and write it to CSV file ')
    status = aem.dam.fetchFolderTree(path='/content/dam/dampy/test', csv_file='output/re_folder_tree.csv')
    logging.debug('Status : '+str(status))

    # Upload an asset. Uploads under /content/dam as path is not specified 
    logging.debug ('Upload an asset at the specified path')
    status = aem.dam.uploadAsset('upload/Shorts_men.jpg')
    logging.debug('Status : '+str(status))

    # Upload an asset at the specified path - dampy/test/samples. 
    logging.debug ('Upload an asset at the specified path')
    status = aem.dam.uploadAsset('upload/Shorts_men.jpg', '/content/dam/dampy/test/samples')
    logging.debug('Status : '+str(status))

    # Upload all assets in a local upload folder to DAM under dampy/test/new_samples. By default uploads all assets from the folder named 'upload' 
    logging.debug ('Upload all assets in a local folder to DAM')
    status = aem.dam.uploadFolder(path='/content/dam/dampy/test/new_samples')
    logging.debug('Status : '+str(status))

    # Upload all assets in a local folder 'upload_test' to DAM under dampy/test/samples.  
    logging.debug ('Upload all assets in a local folder to DAM at the specified path')
    status = aem.dam.uploadFolder(dir='upload/products', path='/content/dam/dampy/test/samples')
    logging.debug('Status : '+str(status))

    # Checkout an asset in DAM
    logging.debug ('Checkout an asset')
    status = aem.dam.checkout('/content/dam/dampy/test/samples/Shorts_men.jpg')
    logging.debug('Status : '+str(status))
    
    # Checkin an asset in DAM
    logging.debug ('Checkin an asset')
    status = aem.dam.checkin('/content/dam/dampy/test/samples/Shorts_men.jpg')
    logging.debug('Status : '+str(status))
    
    # Crop an asset in DAM
    logging.debug ('Crop an asset')
    status = aem.dam.crop('/content/dam/dampy/test/samples/Shorts_men.jpg', (100,100), (500,450))
    logging.debug('Status : '+str(status))
    
    # Rotate an asset in DAM
    logging.debug ('Rotate an asset')
    status = aem.dam.rotate('/content/dam/dampy/test/samples/Shorts_men.jpg', 90)
    logging.debug('Status : '+str(status))
    
    # Flip an asset in DAM horizontally
    logging.debug ('Flipping an asset horizontally')
    status = aem.dam.flip('/content/dam/dampy/test/samples/Shorts_men.jpg', 'h')
    logging.debug('Status : '+str(status))

    # Flip an asset in DAM vertically
    logging.debug ('Flipping an asset vertically')
    status = aem.dam.flip('/content/dam/dampy/test/samples/Shorts_men.jpg', 'vertical')
    logging.debug('Status : '+str(status))

    # Flip an asset in DAM both horizontally & vertically
    logging.debug ('Flipping an asset both horizontally & vertically')
    status = aem.dam.flip('/content/dam/dampy/test/samples/Shorts_men.jpg', 'b')
    logging.debug('Status : '+str(status))

    # Image map an asset in DAM - Circle
    logging.debug ('Image map an asset based on data - Circle')
    status = aem.dam.map('/content/dam/dampy/test/samples/Shorts_men.jpg', data='[circle(482,536,324)"#test_link_c"|"_blank"|"Test link Cricle"]')
    logging.debug('Status : '+str(status))
    
    # Image map an asset in DAM - Rectangle
    logging.debug ('Image map an asset based on data - Rectangle')
    status = aem.dam.map('/content/dam/dampy/test/samples/Shorts_men.jpg', data='[rect(182,36,524,322)"#test_link_p"|"_self"|"Test link Rectangle"]')
    logging.debug('Status : '+str(status))
    
    # Image map an asset in DAM - Rectangle & Circle
    logging.debug ('Image map an asset based on data - Rectangle & Circle')
    status = aem.dam.map('/content/dam/dampy/test/samples/Shorts_men.jpg', data='[rect(182,36,524,322)"test_link_p"|"_self"|"Test link Rectangle"][circle(482,536,324)"test_link_c"|"_blank"|"Test link Cricle"]')
    logging.debug('Status : '+str(status))

    # Edit an asset in DAM - Crop, rotate, filp and map in one go
    logging.debug ('Edit an asset - Crop, rotate, filp and map in one go')
    status = aem.dam.edit('/content/dam/dampy/test/samples/Shorts_men.jpg', crop='87,87,778,551', rotate='270', flip='h', map='[rect(182,36,524,322)"#test_link_p"|"_self"|"Test link Rectangle"][circle(482,536,324)"#test_link_c"|"_blank"|"Test link Cricle"]')
    logging.debug('Status : '+str(status))

    # Download an asset to a local folder. By default gets downloaded to a folder named 'download'
    logging.debug ('Download an asset to a local folder')
    status = aem.dam.downloadAsset('/content/dam/dampy/test/samples/Shorts_men.jpg')
    logging.debug('Status : '+str(status))
    
    # Download an asset to a local folder, retaining the DAM path in local. By default gets downloaded to a folder named 'download'
    logging.debug ('Download an asset to a local folder, retaining the DAM path in local')
    status = aem.dam.downloadAsset('/content/dam/dampy/test/samples/Shorts_men.jpg', retain_dam_path=True)
    logging.debug('Status : '+str(status))

    # Download all assets under a path. By default assets tree get downloaded under a folder named 'download'
    logging.debug ('Download all assets under a path')
    status = aem.dam.downloadFolder('/content/dam/dampy/test/samples')
    logging.debug('Status : '+str(status))

    # Download all assets under a DAM path to local, ignoring the DAM folder tree hierarchy. By default assets tree get downloaded under a folder named 'download'
    logging.debug ('Download all assets under a DAM path to local, ignoring the DAM folder tree hierarchy')
    status = aem.dam.downloadFolder('/content/dam/dampy/test/new_samples', 'download/test', False)
    logging.debug('Status : '+str(status))

    # Get Metadata of an asset
    logging.debug ('Get Metadata of an asset')
    metadata = aem.dam.metadata('/content/dam/dampy/test/samples/Shorts_men.jpg')
    logging.debug(metadata)

    # Extract default properties of assets under the given path and write it to a CSV file
    logging.debug ('Extract properties of assets under the given path and write it to a CSV file')
    status = aem.dam.xprops('/content/dam/dampy/test/samples')
    logging.debug('Status : '+str(status))

    # Extract specific properties of assets under the given path and write it to a CSV file
    logging.debug ('Extract specific properties of assets under the given path and write it to a CSV file')
    status = aem.dam.xprops('/content/dam/dampy/test', ['jcr:path', 'jcr:content/metadata/dc:title','jcr:content/metadata/jcr:title'])
    logging.debug('Status : '+str(status))

    # Update properties of assets based on an input CSV file
    logging.debug ('Update properties of assets based on an input CSV file')
    status = aem.dam.uprops()
    logging.debug('Status : '+str(status))

    # Update properties of assets based on an input CSV file
    logging.debug ('Update properties of assets based on an input CSV file')
    status = aem.dam.uprops('input/my_asset_update.csv')
    logging.debug('Status : '+str(status))

    # Update properties of assets based on an input CSV file
    logging.debug ('Update properties of assets based on an input CSV file, including tag values')
    status = aem.dam.uprops('input/asset_props_tags.csv')
    logging.debug('Status : '+str(status))

    # Extract specific properties of assets under the given path and write it to a CSV file
    logging.debug ('Extract specific properties of assets under the given path and write it to a CSV file')
    status = aem.dam.xprops('/content/dam/dampy/test', ['jcr:path', 'jcr:content/metadata/dc:title','jcr:content/metadata/jcr:title'], 'output/after_my_update.csv')
    logging.debug('Status : '+str(status))

    # Activate an asset
    logging.debug ('Activate an asset')
    status = aem.dam.activate('/content/dam/dampy/test/samples/Shorts_men.jpg')
    logging.debug('Status : '+str(status))

    # Activate a folder
    logging.debug ('Activate a folder')
    status = aem.dam.activate('/content/dam/dampy/test/samples')
    logging.debug('Status : '+str(status))

    # Activate a list of assets in text file
    logging.debug ('Activate a list of assets in text file')
    status = aem.dam.activateList(listSrc='input/alist.txt')
    logging.debug('Status : '+str(status))

    # Activate a list of assets in a CSV file
    logging.debug ('Activate a list of assets in a CSV file')
    status = aem.dam.activateList(listSrc='input/alist.csv')
    logging.debug('Status : '+str(status))

    # Activate a list of assets passed in as parameter
    logging.debug ('Activate a list of assets passed in as parameter')
    status = aem.dam.activateList(listSrc=['/content/dam/dampy/test/new_samples/activities/hiking-camping/alpinists-himalayas.jpg', '/content/dam/dampy/test/new_samples/activities/running/fitness-woman.jpg'])
    logging.debug('Status : '+str(status))

    # Deactivate an asset
    logging.debug ('Deactivate an asset')
    status = aem.dam.deactivate('/content/dam/dampy/test/samples/Shorts_men.jpg')
    logging.debug('Status : '+str(status))

    # Deactivate a folder
    logging.debug ('Deactivate a folder')
    status = aem.dam.deactivate('/content/dam/dampy/test/samples')
    logging.debug('Status : '+str(status))

    # Deactivate a list of assets in text file
    logging.debug ('Deactivate a list of assets in text file')
    status = aem.dam.deactivateList(listSrc='input/alist.txt')
    logging.debug('Status : '+str(status))

    # Deactivate a list of assets in a CSV file
    logging.debug ('Deactivate a list of assets in a CSV file')
    status = aem.dam.deactivateList(listSrc='input/alist.csv')
    logging.debug('Status : '+str(status))

    # Deactivate a list of assets passed in as parameter
    logging.debug ('Deactivate a list of assets passed in as parameter')
    status = aem.dam.deactivateList(listSrc=['/content/dam/dampy/test/new_samples/activities/hiking-camping/alpinists-himalayas.jpg', '/content/dam/dampy/test/new_samples/activities/running/fitness-woman.jpg'])
    logging.debug('Status : '+str(status))

    # Delete an asset
    logging.debug ('Delete an asset')
    status = aem.dam.delete('/content/dam/Shorts_men.jpg')
    logging.debug('Status : '+str(status))

    # Delete a list of assets in text file
    logging.debug ('Delete a list of assets in text file')
    status = aem.dam.deleteList(listSrc='input/alist.txt')
    logging.debug('Status : '+str(status))

    # Delete a list of assets in a CSV file
    logging.debug ('Delete a list of assets in a CSV file')
    status = aem.dam.deleteList(listSrc='input/alist.csv')
    logging.debug('Status : '+str(status))

    # Delete a list of assets passed in as parameter
    logging.debug ('Delete a list of assets passed in as parameter')
    status = aem.dam.deleteList(listSrc=['/content/dam/dampy/test/new_samples/activities/hiking-camping/alpinists-himalayas.jpg', '/content/dam/dampy/test/new_samples/activities/running/fitness-woman.jpg'])
    logging.debug('Status : '+str(status))

    # Delete an asset
    logging.debug ('Delete a folder')
    status = aem.dam.delete('/content/dam/dampy/test')
    logging.debug('Status : '+str(status))

    # Check if an asset exits in DAM and return the paths under which its present 
    logging.debug ('Check if an asset exits (positive) in DAM and return the paths under which its present ')
    status = aem.dam.exists('upload/Shorts_men.jpg')
    logging.debug('Status : '+str(status))

    # Check if an asset exits in DAM and return the paths under which its present 
    logging.debug ('Check if an asset exits (negative) in DAM and return the paths under which its present ')
    status = aem.dam.exists('upload/AEM6.1.jpg')
    logging.debug('Status : '+str(status))

    # List all duplicate assets in DAM under the given path
    logging.debug ('List all duplicate assets in DAM under the given path')
    status = aem.dam.duplicates('/content/dam/dampy')
    logging.debug('Status : '+str(status))

    # List all duplicate assets in DAM
    logging.debug ('List all duplicate assets in DAM')
    status = aem.dam.duplicates()
    logging.debug('Status : '+str(status))
