# -*- coding: utf-8 -*-
import datetime
import os.path
import pathlib
import shutil
import webbrowser
from os.path import abspath
from os.path import dirname
import functions.auxiliary as a

def update_all_directories():
    dirs_path = dirname(dirname(abspath(__file__)))
    with open(dirs_path + '\\config.txt', 'r') as config:
        dirs_path = config.readline().split(',')[1].strip()
    folders = pathlib.Path(dirs_path)
    for d in folders.iterdir():
        a.update_hashes(d)
        
        
def update_directory(d):
    dirs_path = dirname(dirname(abspath(__file__)))
    with open(dirs_path + '\\config.txt', 'r') as config:
        dirs_path = config.readline().split(',')[1].strip()
    a.update_hashes(str(dirs_path) + '\\' + d)
    
    
def delete_directory(d):    
    dirs_path = dirname(dirname(abspath(__file__)))
    with open(dirs_path + '\\config.txt', 'r') as config:
        dirs_path = config.readline().split(',')[1].strip()
    shutil.rmtree(str(dirs_path) + '\\' + d, ignore_errors=True)


def view_excluded(d):
    dirs_path = dirname(dirname(abspath(__file__)))
    with open(dirs_path + '\\config.txt', 'r') as config:
        dirs_path = config.readline().split(',')[1].strip()
    with open(str(dirs_path) + '\\' + d + '\\excluded.txt') as excluded:
        excluded_files = excluded.readlines()
    
    return excluded_files


def manage_excluded(d):
    dirs_path = dirname(dirname(abspath(__file__)))
    with open(dirs_path + '\\config.txt', 'r') as config:
        dirs_path = config.readline().split(',')[1].strip()
    webbrowser.open(dirs_path + '\\' + d + '\\excluded.txt')
                
def check_hashes():
    dirs_path = dirname(dirname(abspath(__file__)))
    
    with open(dirs_path + '\\config.txt', 'r') as config:
        dirs_path = config.readline().split(',')[1].strip()
        logs_path = config.readline().split(',')[1].strip()
        nlogs = int(config.readline().split(',')[1].strip())
    
    logs = list(pathlib.Path(logs_path).iterdir()) 
    if len(logs) >= nlogs:
        logs = logs[0]
        os.remove(str(logs).replace('\\', '\\\\'))
    
    logs_path += '\\' + str(datetime.datetime.today()).split('.')[0].replace(':', '_') + '.txt'
    
    with open(logs_path, 'w+') as log:
        log.write('Checking started\n')
        log.write("System's current date is " + str(datetime.datetime.today()).split('.')[0] + '\n')
    
    folders = pathlib.Path(dirs_path)
    
    for d in folders.iterdir():
        if os.path.isdir(str(d)):
            with open(str(d) + '\\excluded.txt', 'r') as excluded:
                excluded_files = excluded.readlines()
            
            with open(str(d) + '\\dir.txt', 'r') as search:
                files_path = search.readline()
            
            hashes = a.hash_files(files_path, excluded_files)
            
            with open(str(d) + '\\hashes.txt', 'r') as hashes_file:
                with open(logs_path, 'a+') as log:
                    log.write('Checking "' + files_path + '"\n')
                a.check_files(hashes, list(hashes_file), logs_path)