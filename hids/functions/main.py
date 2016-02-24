# -*- coding: utf-8 -*-
import pathlib
import os.path
from os.path import abspath
from os.path import dirname
from functions.auxiliary import hash_files
from functions.auxiliary import check_files

def init_hashes():
    dirs_path = dirname(dirname(abspath(__file__)))
    with open(dirs_path + '\\config.txt', 'r') as config:
        dirs_path = config.readline().split(',')[1].strip()
    folders = pathlib.Path(dirs_path)
    for d in folders.iterdir():
        if os.path.isdir(str(d)):
            with open(str(d) + '\\excluded.txt', 'r') as excluded:
                excluded_files = excluded.readlines()
            with open(str(d) + '\\dir.txt', 'r') as search:
                files_path = search.readline()
            hashes = hash_files(files_path, excluded_files)
            with open(str(d) + '\\hashes.txt', 'w+') as hashes_file:
                hashes_file.writelines('\n'.join(hashes))
                
def check_hashes():
    dirs_path = dirname(dirname(abspath(__file__)))
    with open(dirs_path + '\\config.txt', 'r') as config:
        dirs_path = config.readline().split(',')[1].strip()
    folders = pathlib.Path(dirs_path)
    for d in folders.iterdir():
        if os.path.isdir(str(d)):
            with open(str(d) + '\\excluded.txt', 'r') as excluded:
                excluded_files = excluded.readlines()
            with open(str(d) + '\\dir.txt', 'r') as search:
                files_path = search.readline()
            hashes = hash_files(files_path, excluded_files)
            with open(str(d) + '\\hashes.txt', 'r') as hashes_file:
                check_files(hashes, list(hashes_file))
                
    
check_hashes()