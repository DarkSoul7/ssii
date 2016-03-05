# -*- coding: utf-8 -*-
import datetime
import os.path
import pathlib
from os.path import abspath
from os.path import dirname
import hids.functions.auxiliary as a
from hids.functions import cryptography


def update_all_directories():
    dirs_path = dirname(dirname(abspath(__file__)))
    with open(dirs_path + '\\config.txt', 'r') as config:
        dirs_path = config.readline().split(',')[1].strip()
    folders = pathlib.Path(dirs_path)
    for d in folders.iterdir():
        a.update_hashes(str(d).encode(encoding='utf-8'))
        
        
def update_directory(d):
    dirs_path = dirname(dirname(abspath(__file__)))
    with open(dirs_path + '\\config.txt', 'r') as config:
        dirs_path = config.readline().split(',')[1].strip()
    a.update_hashes(str(dirs_path) + '\\' + d)


def view_excluded(d):
    dirs_path = dirname(dirname(abspath(__file__)))
    with open(dirs_path + '\\config.txt', 'r') as config:
        dirs_path = config.readline().split(',')[1].strip()
    excluded_files = cryptography.decrypt_file(str(dirs_path) + '\\' + d + '\\excluded.txt')

    return excluded_files.split('\n') if excluded_files else None


def view_files(d):
    dirs_path = dirname(dirname(abspath(__file__)))
    with open(dirs_path + '\\config.txt', 'r') as config:
        dirs_path = config.readline().split(',')[1].strip()
    hashes = cryptography.decrypt_file(str(dirs_path) + '\\' + d + '\\hashes.txt')
    hashes = hashes.split('\n')
    stored_files = [file.split(',')[0].split('\\')[-1] for file in hashes]
    
    return stored_files if stored_files[0] else None


def view_config_file():
    dirs_path = dirname(dirname(abspath(__file__)))
    with open(dirs_path + '\\config.txt', 'r') as config:
        config_file = config.readlines()
    
    return config_file


def manage_excluded(d, excluded):
    res = True

    try:
        dirs_path = dirname(dirname(abspath(__file__)))
        with open(dirs_path + '\\config.txt', 'r') as config:
            dirs_path = config.readline().split(',')[1].strip()
        cryptography.encrypt_file(excluded, dirs_path + '\\' + d + '\\excluded.txt')
    except:
        res = False

    return res


def check_hashes():
    analysed_files = 0
    failed_files = 0
    previous_log = None
    dirs_path = dirname(dirname(abspath(__file__)))
    
    with open(dirs_path + '\\config.txt', 'r') as config:
        dirs_path = config.readline().split(',')[1].strip()
        logs_path = config.readline().split(',')[1].strip()
        nlogs = int(config.readline().split(',')[1].strip())
    
    logs = list(pathlib.Path(logs_path).iterdir()) 
    if len(logs) >= nlogs:
        while len(logs) >= nlogs:
            os.remove(str(logs[0]).replace('\\', '\\\\'))
            logs.remove(logs[0])
    
    if len(logs) > 0:
        previous_log = str(logs[-1]).replace('\\', '\\\\')
    
    logs_path += '\\' + str(datetime.datetime.today()).split('.')[0].replace(':', '_') + '.txt'
    
    with open(logs_path, mode='w+', encoding='utf-8') as log:
        log.write('Checking started\n')
        log.write("System's current date is " + str(datetime.datetime.today()).split('.')[0] + '\n')
    
    folders = pathlib.Path(dirs_path)
    
    for d in folders.iterdir():
        if os.path.isdir(str(d)):
            excluded_files = cryptography.decrypt_file(str(d) + '\\excluded.txt').split('\n')
            files_path = cryptography.decrypt_file(str(d) + '\\dir.txt')

            hashes = a.hash_files(files_path, excluded_files)
            hashes_file = cryptography.decrypt_file(str(d) + '\\hashes.txt').split('\n')

            with open(logs_path, mode='a+', encoding='utf-8') as log:
                log.write('Checking "' + files_path + '"\n')
            (analysed, failed) = a.check_files(hashes, list(hashes_file), logs_path)
            analysed_files += analysed
            failed_files += failed
    
    with open(logs_path, mode='a+', encoding='utf-8') as log:
        log.write('Analysed files: ' + str(analysed_files) + '\n')
        log.write('Failed files: ' + str(failed_files) + '\n')
        success_files = analysed_files - failed_files
        ratio = success_files*1.0/analysed_files
        log.write('Daily Integrity Conformity Ratio: ' + str(ratio) + '\n')
        
        if previous_log:
            try:
                with open(previous_log) as previous_log_file:
                    previous_log = previous_log_file.readlines()
                    previous_log = float(previous_log[-3].split(':')[1][:-2])
                log.write('Previous Integrity Conformity Ratio: ' + str(previous_log) + '\n')
                log.write('Trend: ' + 'POSITIVE' if ratio >= previous_log else 'NEGATIVE')
            except:
                log.write('Previous Integrity Conformity Ratio: -\n')
                log.write('Trend: ' + 'POSITIVE')
        else:
            log.write('Previous Integrity Conformity Ratio: -\n')
            log.write('Trend: ' + 'POSITIVE')