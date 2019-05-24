def trimPath(path):
    if path.endswith('/'):
        return path[:-1]
    return path

def splitPath(path):
    #Get path & name of the asset
    name = path[path.rindex('/')+1:]
    parent = path[:path.rindex('/')]
    return parent,name

def cleansePaths(dir, files):
    c_files = {}
    for file in files:
        p, v = file.split(dir, 1)
        if not v.startswith('/content/dam/'):
            v = '/content/dam' + v
        parent, name = splitPath(v)
        c_files[file] = parent
    return c_files

