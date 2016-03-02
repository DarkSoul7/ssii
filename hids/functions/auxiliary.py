# -*- coding: utf-8 -*-
import hashlib
import pathlib
import os.path
import re
from os.path import abspath
from os.path import dirname


def create_hash(path):
    with open(path, 'r') as message:
        h = hashlib.sha512(str(message).encode()).hexdigest()
    return h

    
def scan_files(path, excluded_files):
    directory = pathlib.Path(path)
    files = []
    
    for d in directory.iterdir():
        d  = str(d)
        if os.path.isfile(d):
            if d not in excluded_files:
                files.append(d)
    
    return files


def hash_files(path, excluded_files):
    dirs = scan_files(path, excluded_files)
    hashes = [str(d) + ',' + create_hash(str(d)) for d in dirs]
    return hashes
            

def check_files(newHashes, storedHashes, logs_file):
    newHashes = [newHashes[i].split(',') for i in range(0, len(newHashes))]
    storedHashes = [storedHashes[i].split(',') for i in range(0, len(storedHashes))]
    dicNew = {newHash[0]: newHash[1].strip() for newHash in newHashes}
    dicStored = {storedHash[0]: storedHash[1].strip() for storedHash in storedHashes}
    
    with open(logs_file, 'a+') as log:
        if len(dicNew.keys()) != len(dicStored.keys()):
            log.write('[ERROR] The number of stored files does not match the current number of files in this directory\n')
        
        if len(dicNew.keys()) > len(dicStored.keys()):
            for key in dicNew.keys():
                if key not in dicStored.keys():
                    log.write('[ERROR] "' + key + '" has been added to this directory and is not under version control\n')
                elif dicNew[key] != dicStored[key]:
                    log.write('[ERROR] "' + key + '" has been modified\n')
        else:
            for key in dicStored.keys():
                if key not in dicNew.keys():
                    log.write('[ERROR] "' + key + '" has been deleted from this directory\n')
                elif dicNew[key] != dicStored[key]:
                    log.write('[ERROR] "' + key + '" has been modified\n')
        
        log.write('Directory checked\n')
            
            
def new_directory(path, dir_name=''):
    res = True
    try:
        if not dir_name:
            dirs_path = dirname(dirname(abspath(__file__)))
            with open(dirs_path + '\\config.txt', 'r') as config:
                lines = config.readlines()
                dir_name = lines[3].split(',')[1].strip()
                lines[3] = 'nextDir,dir' + str(int(" ".join(re.findall("[0-9]+", dir_name)))+1) + '\n'
                out = open(dirs_path + '\\config.txt', 'w')
                out.writelines(lines)
                out.close()
        
        new_dir_path = dirs_path + '\\files\\directories\\' + dir_name  
        os.makedirs(new_dir_path)
        with open(str(new_dir_path) + '\\dir.txt', 'w+') as d:
            d.writelines(path)
        excluded = open(str(new_dir_path) + '\\excluded.txt', 'w+')
        excluded.close()
        with open(str(new_dir_path) + '\\hashes.txt', 'w+') as hashes_file:
            hashes = hash_files(path, '')
            hashes_file.writelines('\n'.join(hashes))
    except:
        res = False
    
    return res


def update_hashes(d):
    if os.path.isdir(str(d)):
        with open(str(d) + '\\excluded.txt', 'r') as excluded:
            excluded_files = excluded.readlines()
        with open(str(d) + '\\dir.txt', 'r') as search:
            files_path = search.readline()
        hashes = hash_files(files_path, excluded_files)
        with open(str(d) + '\\hashes.txt', 'w+') as hashes_file:
            hashes_file.writelines('\n'.join(hashes))


def update_time(time):
    res = True
    try:
        dirs_path = dirname(dirname(abspath(__file__)))
        with open(dirs_path + '\\config.txt', 'r') as config:
            lines = config.readlines()
            lines[4] = 'time,' + time + '\n'
            out = open(dirs_path + '\\config.txt', 'w')
            out.writelines(lines)
            out.close()
    except:
        res = False
    
    return res


def update_nlogs(nlogs):
    res = True
    try:
        dirs_path = dirname(dirname(abspath(__file__)))
        with open(dirs_path + '\\config.txt', 'r') as config:
            lines = config.readlines()
            lines[2] = 'nlogs,' + nlogs + '\n'
            out = open(dirs_path + '\\config.txt', 'w')
            out.writelines(lines)
            out.close()
    except:
        res = False
    
    return res


def get_directories():
    res = []
    dirs_path = dirname(dirname(abspath(__file__))) + '\\files\\directories'
    directories = pathlib.Path(dirs_path)
    dirs = directories.iterdir()
    for d in dirs:
        with open(str(d) + '\\dir.txt', 'r') as file:
            res.append((str(d).split('\\')[-1].strip(), file.readline().strip()))
    return res