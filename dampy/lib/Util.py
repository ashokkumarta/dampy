# ashokkumar.ta@gmail.com / 24-May-2019

import os, re

def trimPath(path):
    '''
    Removes the trailing / from the path given
    >>> trimPath('/content/dam/sample/')
    /content/dam/sample
    '''
    if path.endswith('/'):
        return path[:-1]
    return path

def splitPath(path):
    '''
    Splits the path given into parent path and file name
    >>> trimPath('/content/dam/sample/test.png')
    ('/content/dam/sample', 'test.png')
    '''
    #Get path & name of the asset
    name = path[path.rindex('/')+1:]
    parent = path[:path.rindex('/')]
    return parent,name

def cleansePaths(dir, files, path):
    '''
    Removes the dir prefix from the names of the files, check each file if it starts with 
    /content/dam and if not pre-pends the path to the file
    Finally takes the parent path of the files and retuns a dict mapping files given to the parent path
    '''
    c_files = {}
    for file in files:
        p, v = file.split(dir, 1)
        if not v.startswith('/content/dam/'):
            v = path + v
        parent, name = splitPath(v)
        c_files[file] = namify(parent)
    return c_files

def cleanseDirList(baseDir, dirList, path):
    '''
    Removes the baseDir prefix from the names in the dirList, check each dir if it starts with 
    /content/dam and if not pre-pends the path to the file and returns it
    '''
    l_dirs = []
    for dir in dirList:
        if baseDir:
            p, v = dir.split(baseDir, 1)
        else:
            v = dir
        if not v.startswith('/content/dam/'):
            if not (v.startswith('/') or path.endswith('/')):
                v = path + '/' + v
            else:
                v = path + v
                v = re.sub('//','/',v)
        l_dirs.append(v)
    return l_dirs

def dir_n_file(path, ext):
    base = os.path.basename(path)
    dir = os.path.dirname(path)
    if not base.endswith('.'+ext):
        base += '.'+ext
    if not dir:
        dir = '.'
    return dir, base

def namify(path):
    return re.sub('[ %:*?"\'|.#{}^;+,$]','-',path).lower()

