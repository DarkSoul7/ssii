#encode: utf-8
import hashlib
import pathlib
import os.path
from os.path import abspath
from os.path import dirname


files_dir = dirname(dirname(abspath(__file__)))
if os.name == 'nt':
    file_hashes = files_dir + r'\files\hashes.txt'
    file_excluded = files_dir + r'\files\excluded.txt'
else:
    file_hashes = files_dir + '/files/hashes.txt'
    file_excluded = files_dir + '/files/excluded.txt'


def create_hash(message):
    sha = hashlib.sha512(message.encode())
    return sha.hexdigest()

    
def scan_files(path, excluded_files):
    directory = pathlib.Path(path)
    files = []
    
    for d in directory.iterdir():
        d  = str(d)
        if d not in excluded_files:
            if os.path.isdir(str(d)):
                files.extend(scan_files(d, excluded_files))
            else:
                files.append(d)
    
    return files


def hash_files(path, excluded_files):
    dirs = scan_files(path, excluded_files)
    hashes = [d + ',' + create_hash(str(d)) for d in dirs]
    return hashes


def check_files(newHashes, storedHashes):
    newHashes = [newHashes[i].split(',') for i in range(0, len(newHashes))]
    storedHashes = [storedHashes[i].split(',') for i in range(0, len(storedHashes))]
    dicNew = {newHash[0]: newHash[1].strip() for newHash in newHashes}
    dicStored = {storedHash[0]: storedHash[1].strip() for storedHash in storedHashes}
    
    if len(dicNew.keys()) != len(dicStored.keys()):
        print(r'El numero de archivos actual no coincide con el de la base de datos. Si ha actualizado el directorio, actualice la base de datos, por favor');
    else:
        bool = True
        for key in dicNew.keys():
            if dicNew[key] != dicStored[key]:
                print('El fichero ', key, ' ha sido modificado.')
                bool = False
                break
        if bool:
            print('Todo correcto')


def exclude_files(files, excluded_path):
    file = open(excluded_path, 'w+')
    file.writelines('\n'.join(files))
    file.close()

    
def exclude_path(path, excluded_path):
    file = open(excluded_path, 'w+')
    file.writelines(path)
    file.close()