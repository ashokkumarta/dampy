import os, json
import logging

class _Config:

    def __getitem__(self, key):
        return self._config_json[key]

    def __getattr__(self, attr):
        return self.__getitem__(attr)

    def __init__(self, config_json):
        logging.debug('Loading the configuration')
        self._config_json = config_json

keys = _Config({
    "assets_key": "hits",
    "path_key": "jcr:path", 
    "sha1_key": "jcr:content/metadata/dam:sha1"
})

urls = _Config({
    "list": "/bin/querybuilder.json?type=dam:Asset&p.limit=-1&p.hits=selective&p.properties=jcr:path&p.nodedepth=-1&path=",
    "xprops": "/bin/querybuilder.json?type=dam:Asset&p.limit=-1&p.hits=selective&p.properties=$props&p.nodedepth=-1&path=",
    "fetchFolderTree": "/bin/querybuilder.json?type=sling:Folder&p.limit=-1&p.hits=selective&p.properties=$props&p.nodedepth=-1&path=",
    "uprops": "/content/dam.html",
    "metadata_suffix": "/jcr:content.",
    "metadata_type": ".json",
    "activate": "/bin/replicate.json",
    "deactivate": "/bin/replicate.json",
    "checkout": ".checkout.json",
    "edit": ".assetimage.html",
    "move": "/bin/wcmcommand",
    "updateFolderTitle": "/content/dam",
    "delete": "/bin/wcmcommand",
    "exists": "/bin/querybuilder.json?p.hits=selective&path=/content/dam&p.properties=jcr:path&p.limit=-1&property=jcr:content/metadata/dam:sha1&property.operation=equals&property.value=",
    "duplicates": "/bin/querybuilder.json?p.hits=selective&p.properties=jcr:path jcr:content/metadata/dam:sha1&p.limit=-1&property=jcr:content/metadata/dam:sha1&property.operation=exists&path=",
    "activateTree": "/libs/replication/treeactivation.html"
})

msgs = _Config({
    "createFolder" : "{\"./jcr:primaryType\": \"sling:OrderedFolder\", \"./jcr:content/jcr:primaryType\": \"nt:unstructured\", \"./jcr:content/jcr:title\":\"$title\", \":name\":\"$name\" }",
    "move" : "{\"cmd\": \"movePage\", \"integrity\": \"true\", \"srcPath\":\"$srcPath\", \"destParentPath\":\"$destParentPath\", \"destName\":\"$destName\" }",
    "updateFolderTitle" : "{\":operation\": \"dam.share.folder\", \"path\":\"$path\",            \"title\":\"$title\" }",
    "delete" : "{\"cmd\": \"deletePage\", \"path\":\"$path\", \"force\":\"force\"}",
    "activate" : "{\"cmd\": \"Activate\", \"path\":\"$path\", \"force\":\"force\"}",
    "deactivate" : "{\"cmd\": \"Deactivate\", \"path\":\"$path\", \"force\":\"force\"}",
    "checkout" : "{\"action\": \"checkout\"}",
    "checkin" : "{\"action\": \"checkin\"}",
    "edit" : "{\"./crop\": \"$crop\", \"./rotate\": \"$rotate\", \"./flipHorizontal\": \"$flipHorizontal\", \"./flipVertical\": \"$flipVertical\", \"./imageMap\": \"$imageMap\"}",
    "uprops" : "[(\"_charset_\", \"utf-8\"), (\"dam:bulkUpdate\", \"true\"), (\"mode\", \"hard\")]"

})
