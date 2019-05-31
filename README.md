# dampy							
An utility to easily work with Adobe Experience Manager (AEM) DAM. 

## Dependencies
```
Python 3
```

## About the tool
dampy is a tool to work with AEM DAM. For a client I recently work with, as we went live the client team had frequent requests to
* Get a list of all the assets under a path 
* Download all assets under a path
* Upload assets organized in the local folder structure to DAM
* Extract specific properties of all assets under a path
* Update properties of assets based on spreadsheet
* And so on…

After dabbling with curls, AEM reports and WebDAV tools, I came to realize that writing Python scripts to make REST API calls to AEM and/or convert the result JSON into required output format to be the quickest and easiest option to handle these requests. 

dampy is a consolidation of many such scripts written into a comprehensive tool to work with AEM DAM 


## Getting Started
dampy is available as pip install. To start working on this tool install it through pip command

```
pip install dampy
```

After the tool is installed, you can straight away start using it. All that it takes is to import AEM class from dampy package and start working with it. The below code is all it takes to get a list of all assets in DAM


```
# Getting started

# Import AEM from dampy.AEM
>>> From dampy.AEM import AEM

# Create a handle to an AEM Instance
>>> author = AEM()

# List all assets in DAM
>>> author.dam.list()
```

As you can see, three lines is all it takes to get a list of all assets in DAM
1.	Import AEM from dampy.AEM
2.	Create an instance of AEM
3.	Call the list method 

__Note:__ By default, dampy connects to AEM Author instance running locally with admin/admin as credentials. Keep your local AEM instance running when trying the above snippet. 

## dampy in-depth
The following sections explains in-depth the functionalities and technical details of dampy tool

### Creating an AEM handle
The first step in working with dampy is to create an AEM handle. To create an AEM handle, import AEM from dampy.AEM and create an instance of it. Below code snippet shows various options to create an AEM handle

```
>>> From dampy.AEM import AEM
# Different options for creating AEM handle
# Create AEM handle to default AEM instance
>>> aem = AEM()

# Create AEM handle to the given host and credentials
>>> aem = AEM(‘http://my-aem-host:port’, ‘user’,’password’)

# Create AEM handle to default host, for admin user with password as ‘new-password’
>>> aem = AEM(password = ‘new-password’)
```

As you can see, AEM constructor takes in three optional parameters

__host__ – defaults to http://localhost:4502
__user__ – defaults to ‘admin’
__password__ – defaults to ‘admin’

You can pass in none, all three, or some of these parameters to create an AEM handle

### The dam object in AEM handle
The AEM handle includes a dam object wrapped within it and all functionalities of dampy are exposed as methods on this dam object. The signature for invoking any method on dam looks like this

```
>>> aem.dam.<api>(<params...>)
```

We will see all the methods exposed on dam object in the following sections


### list()

This method takes an optional path parameter and returns a list of all assets under this path. The returned list includes assets under all the subfolders of this path, subfolders under it and so on covering the entire node tree under the given path

If path parameter is not provided, it returns all assets in DAM (all assets under /content/dam)

It also has two more optional parameters

__csv_dump__ – A Boolean flag indicating if the list needs to be written to a CSV file. Default value of this flag is False

__csv_file__ – The output csv file name to write the list output to. The list gets written to output if either the csv_dump is set to True of csv_file value is specified. 

If csv_dump is set to True but no csv_file value is specified, output is written to the file 'output/asset_list.csv' under the current working directory
 
```
# List all assets under ‘/content/dam/my_folder’
>>> my_assets = aem.dam.list(‘/content/dam/my_folder’)

# List all assets under ‘/content/dam’
>>> all_assets = aem.dam.list()

# List all assets under ‘/content/dam/my_folder’ and also write the output to a CSV file
>>> my_assets = aem.dam.list(‘/content/dam/my_folder’, csv_dump=True)

# List all assets under ‘/content/dam/my_folder’ and also write the output to the CSV file specified
>>> my_assets = aem.dam.list(‘/content/dam/my_folder’, csv_file=’output/list.csv’, )
```

### createFolder()
This method creates a new folder in DAM. It takes in the path of the folder to create as a parameter and an optional title for the folder & returns a Boolean value indicating the success status of folder creation
Parameters 
__path__ – DAM folder path to create
__title__ – Optional title for the folder. If not provided, name of the folder is set as title

```
# Create a new DAM folder /content/dam/new_folder and set its title to ‘new_folder’
>>> status = aem.dam.createFolder(‘/content/dam/new_folder’)

# Create a new DAM folder /content/dam/new_folder and set its title to ‘My New Folder’
>>> status = aem.dam.createFolder(‘/content/dam/new_folder’, ‘My New Folder’)
```

### uploadAsset()
This method uploads an asset from the local path to DAM under the path specified. It takes in 2 parameters

__file__ – Path of the local file to upload. This is a mandatory parameter

__path__ – DAM path under which the file has to be uploaded, Defaults to ‘/content/dam’ if not specified

This method returns a Boolean value indicating the success status

```
# Upload the given file to the specified DAM folder
>>> status = aem.dam.uploadAsset(‘./assets/sample1.png’, ‘/content/dam/new_folder)

# Upload the given file to DAM under ‘/content/dam’
>>> status = aem.dam.uploadAsset(‘./assets/sample1.png’)
```

### uploadFolder()
This method uploads all the assets from a local folder to DAM. It takes in 2 parameters

__dir__ – The local folder path, all assets under which gets uploaded to DAM. This is an optional parameter and uploads all assets under folder named ‘upload’ under the current path if not specified

__path__ – DAM path under which to download. Its optional and defaults to /content/dam. For assets under the folder structure starting with /content/dam/… in the local folder specified, this parameter is ignored

The folder structure under the given local folder dir gets reflected under the DAM path provided. 

This method also returns a Boolean value indicating the success status

```
# Upload all the folders and assets under ./upload to DAM under /content/dam
>>> status = aem.dam.uploadFolder()

# Upload all the folders and assets under ./upload to DAM under /content/dam/my_uploads
>>> status = aem.dam.uploadFolder(path=’/content/dam/my_uploads)

# Upload all the folders and assets under ./assets to DAM under /content/dam
>>> status = aem.dam.uploadFolder(‘./assets’)

# Upload all the folders and assets under ./assets to DAM under /content/dam/my_uploads
>>> status = aem.dam.uploadFolder(dir=‘./assets’, path=’/content/dam/my_uploads)
```


### downloadAsset()
This method downloads the given assets to a local folder. This method takes in three parameters 

__asset_path__ – A mandatory parameter which is the full path to the asset to download

__dir__ – local folder path to download the asset. This is optional and the asset gets downloaded to a folder named ‘download’ if not specified. The folder gets created is the given folder does not exist on the file system

__retain_dam_path__ – A Boolean flag to retain or ignore the DAM folder tree when downloading to local. Defaults to False

This method returns a Boolean value indicating the success or failure of the download

```
# Download the asset to ./download folder
>>> status = aem.dam.downloadAsset(‘/content/dam/my_folder/dampy_sample.png’)

# Download the asset to ./assets folder
>>> status = aem.dam.downloadAsset(‘/content/dam/my_folder/dampy_sample.png’, ‘./assets’)

# Download the asset to ./assets folder under the subfolder /content/dam/my_folder
>>> status = aem.dam.downloadAsset(‘/content/dam/my_folder/dampy_sample.png’, ‘./assets’, True)
```

### downloadFolder()
This method downloads all the assets under a given DAM path to a local folder. This method takes in three parameters 

__path__ – Optional. Path of the DAM folder from which all assets gets downloaded. If this parameter is not given all assets under ‘/content/dam’ gets downloaded

__dir__ – local folder path to download all the asset to. This is optional and the assets get downloaded to a folder named ‘download’ if not specified. The folder to download the assets to gets created if it does not already exist on the file system. 

__retain_dam_path__ – A Boolean flag to retain or ignore the DAM folder tree when downloading to local. Defaults to True

The tree structure of DAM is retained when downloading assets under the given DAM path, with the downloaded folder structure reflecting the DAM folder hierarchy

This method also returns a Boolean value indicating the success or failure of the download

```
# Download all assets under the given DAM folder to ./download, retaining the DAM folder structure in local

>>> status = aem.dam.downloadFolder(‘/content/dam/my_folder’)

# Download all assets under the given DAM folder to ./assets folder, retaining the DAM folder structure in local
>>> status = aem.dam.downloadFolder(‘/content/dam/my_folder’, ‘./assets’)

# Download all assets under the given DAM folder to ./assets folder. All assets are placed in ./assets folder, ignoring the DAM folder structure
>>> status = aem.dam.downloadFolder(‘/content/dam/my_folder’, ‘./assets’, False)
```


### metadata()
This method returns the metadata of the given asset as a json object. It takes in 2 parameters 
asset_path – A mandatory parameter which is the full path to the asset

__level__ – optional, the nesting level in the node hierarchy includes in the response json. Defaults to 1 

```
# Get level 1 metadata of given asset
>>> metadata_json = aem.dam.metadata(‘/content/dam/my_folder/dampy_sample.png’)

# Get up to level 4 metadata of the given asset 
>>> metadata_json = aem.dam.metadata(‘/content/dam/my_folder/dampy_sample.png’, 4)
```

### xprops()
This method extracts the metadata properties of all the assets under a given path and writes it to a CSV file. It takes 3 parameters, all optional

__path__ – DAM path. Extracts properties of all assets under this path. Defaults to ‘/content/dam’

__props__ – List of properties to extract. By default extract the asset path & title

__csv_file__ – The output file to write the extracted properties to. By default, its written to the file ‘output/asset_props.csv’


```
# Extract path and title of all dam assets and write it to output/asset_props.csv
>>> status = aem.dam.xprops()

# Extract path and title of all dam assets under my_folder and write it to output/asset_props.csv
>>> status = aem.dam.xprops(‘/content/dam/my_folder’)

# Extract path, title and tags of all dam assets under my_folder and write it to output/asset_title_n_tags_.csv
>>> status = aem.dam.xprops(‘/content/dam/my_folder’, [‘jcr:path’, ‘jcr:content/metadata/dc:title’, ‘jcr:content/metadata/cq:tags’], ‘output/asset_title_n_tags_.csv’)
```


### uprops()
This method takes a csv file as input and updates asset properties with the data provided in this CSV file. It takes 1parameter, the path to the CSV file. 

__csv_file__  – Path to the csv file with data for asset properties update. By default, tries the read the input csv file at in ‘input/asset_props.csv’

This input CSV file should adhere to the below conditions

* The first row is the header and should have the property name to update for the respective columns. Property name is the fully qualified name of the property under the asset. E.g. Title property name is ‘jcr:content/metadata/dc:title’
* The second row is the type of the property. Can be String, Date, Boolean, … and can be a single value or array value. E.g. for String array mention the type as ‘String[]’
* From row 3 onwards, each row contains the properties for one asset 
* The first column must be ‘jcr:path’ property with its type as String and values as full path of the asset in DAM 

After creating the csv and placing it in a path, invoke the uprops method as given in the below code snippet


```
# Update properties based on the input csv file input/asset_props.csv
>>> status = aem.dam.uprops()

# Update properties based on the input csv file input/asset_cust_props.csv
>>> status = aem.dam.uprops(‘input/asset_cust_props.csv’)
```


### activate()
This method activates the given asset or a folder in DAM. It takes in one mandatory path parameter 

__path__ – Mandatory parameter specifying the path to the asset or DAM folder that needs to be activated

This method returns a Boolean value indicating the success status

```
# Activates the given asset in DAM
>>> status = aem.dam.activate((‘/content/dam/my_folder/dampy_sample.png’)

# Activates the given folder (folder tree) in DAM
>>> status = aem.dam.activate((‘/content/dam/my_folder’)
```

### deactivate()
This method deactivates a given asset or a folder in DAM.  It takes in one mandatory path parameter 

__path__ – Mandatory parameter specifying the path to the asset or a DAM folder that needs to be deactivated

This method returns a Boolean value indicating the success status

```
# Deactivates the given asset in DAM
>>> status = aem.dam.deactivate((‘/content/dam/my_folder/dampy_sample.png’)

# Deactivates the given folder in DAM
>>> status = aem.dam.deactivate((‘/content/dam/my_folder’)
```

### delete()
This method deletes a given asset or a folder. It takes in one mandatory path parameter 

__path__ – Mandatory parameter specifying the path to the asset or the DAM folder that needs to be deleted

This method returns a Boolean value indicating the success status

```
# Deletes the given asset from DAM
>>> status = aem.dam.delete((‘/content/dam/my_folder/dampy_sample.png’)

# Deletes the given folder from DAM
>>> status = aem.dam.delete((‘/content/dam/my_folder’)
```


## Reservation
> Though this is a generic utility, they have been tested for limited set of use cases. Make sure its tested for your scenarios before applying it for production purpose

---
> Environments Tested on:  AEM 6.1, 6.2 & 6.4 | Windows, RHEL5 | Python 3.7.2
