# -*- coding: utf-8 -*-
import hashlib
import pathlib
import os.path
import re
import shutil
from os.path import abspath
from os.path import dirname
from hids.functions import scheduler
from hids.functions import cryptography


def create_hash(path):
    with open(path, mode='rb') as message:
        h = hashlib.sha512(message.read()).hexdigest()
    return h


def scan_files(path, excluded_files):
    directory = pathlib.Path(path)
    files = []

    for d in directory.iterdir():
        d = str(d)
        if os.path.isfile(d):
            if d not in excluded_files:
                files.append(d)

    return files


def hash_files(path, excluded_files):
    dirs = scan_files(path, excluded_files)
    hashes = [str(d) + ',' + create_hash(str(d)) for d in dirs]
    return hashes


def check_files(new_hashes, stored_hashes, logs_file):
    analysed_files = 0
    failed_files = 0
    new_hashes = [new_hashes[i].split(',') for i in range(0, len(new_hashes))]
    stored_hashes = [stored_hashes[i].split(',') for i in range(0, len(stored_hashes))]
    dic_new = {new_hash[0]: new_hash[1].strip() for new_hash in new_hashes}
    dic_stored = {stored_hash[0]: stored_hash[1].strip() for stored_hash in stored_hashes}
    check_list = set(dic_stored.keys()).intersection(set(dic_new.keys()))
    deleted_list = set(dic_stored.keys()).difference(set(dic_new.keys()))
    added_list = set(dic_new.keys()).difference(set(dic_stored.keys()))

    with open(logs_file, mode='a+', encoding='utf-8') as log:
        if deleted_list or added_list:
            log.write('[ERROR] The stored files does not match the current files in this directory\n')

        for deleted in deleted_list:
            log.write('[ERROR] "' + deleted + '" has been deleted from this directory\n')
            failed_files += 1
            analysed_files += 1

        for added in added_list:
            log.write('[ERROR] "' + added + '" has been added to this directory and is not under version control\n')
            failed_files += 1
            analysed_files += 1

        for key in check_list:
            if dic_new[key] != dic_stored[key]:
                log.write('[ERROR] "' + key + '" has been modified\n')
                failed_files += 1

            analysed_files += 1

        log.write('Directory checked\n')

    return analysed_files, failed_files


def new_directory(path, dir_name=''):
    res = True
    try:
        if not dir_name:
            dirs_path = dirname(dirname(abspath(__file__)))
            with open(dirs_path + '\\config.txt', 'r') as config:
                lines = config.readlines()
                dir_name = lines[4].split(',')[1].strip()

        new_dir_path = dirs_path + '\\files\\directories\\' + dir_name
        os.makedirs(new_dir_path)

        cryptography.encrypt_file(path, new_dir_path + '\\dir.txt')
        cryptography.encrypt_file('', new_dir_path + '\\excluded.txt')
        cryptography.encrypt_file('', new_dir_path + '\\hashes.txt')

    except:
        delete_directory(dir_name)
        res = False
    if res:
        with open(dirs_path + '\\config.txt', 'w') as config:
            lines[4] = 'nextDir,dir' + str(int(" ".join(re.findall("[0-9]+", dir_name)))+1) + '\n'
            config.writelines(lines)

    return res


def delete_directory(d):
    dirs_path = dirname(dirname(abspath(__file__)))
    with open(dirs_path + '\\config.txt', 'r') as config:
        dirs_path = config.readline().split(',')[1].strip()
    shutil.rmtree(str(dirs_path) + '\\' + d, ignore_errors=True)


def update_hashes(d):
    res = True

    try:
        if os.path.isdir(str(d)):
            excluded_files = cryptography.decrypt_file(str(d) + '\\excluded.txt')
            files_path = cryptography.decrypt_file(str(d) + '\\dir.txt')
            hashes = hash_files(files_path, excluded_files)
            cryptography.encrypt_file('\n'.join(hashes), str(d) + '\\hashes.txt')
    except:
        res = False

    return res


def update_time(time):
    res = True
    try:
        dirs_path = dirname(dirname(abspath(__file__)))
        with open(dirs_path + '\\config.txt', 'r') as config:
            lines = config.readlines()
            lines[5] = 'time,' + time + '\n'
            out = open(dirs_path + '\\config.txt', 'w')
            out.writelines(lines)
            out.close()
        scheduler.schedule(time)
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


def update_threshold(threshold):
    res = True
    try:
        assert threshold >= 0
        assert threshold <= 100
        dirs_path = dirname(dirname(abspath(__file__)))
        with open(dirs_path + '\\config.txt', 'r') as config:
            lines = config.readlines()
            lines[3] = 'threshold,' + str(threshold) + '\n'
            out = open(dirs_path + '\\config.txt', 'w')
            out.writelines(lines)
            out.close()
    except:
        res = False
    
    return res


def get_directories():
    try:
        res = []
        config_path = dirname(dirname(abspath(__file__))) + '\\config.txt'
        with open(config_path) as config:
            dirs_path = config.readline().split(',')[1].strip()
        directories = pathlib.Path(dirs_path)
        dirs = directories.iterdir()
        for d in dirs:
            file = cryptography.decrypt_file(str(d) + '\\dir.txt')
            res.append((str(d).split('\\')[-1].strip(), file))
    except:
        res = None

    return res
