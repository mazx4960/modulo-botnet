from . import module_class
from .models import Agent, Session, Agent_session, Output

import pickle
import os


PICKLE_DIR = 'apps/api/pickles'
ERR_IDENTIFIER = '[!] Error'


def store_data(data, session_id):
    filename = 'pickle_{}'.format(session_id)
    filepath = os.path.join(PICKLE_DIR, filename)
    with open(filepath, 'wb') as pickle_file:
        pickle.dump(data, pickle_file)


def load_data(session_id):
    filename = 'pickle_{}'.format(session_id)
    filepath = os.path.join(PICKLE_DIR, filename)
    with open(filepath, 'rb') as pickle_file:
        data = pickle.load(pickle_file)
    return data


def output_error(err, session_id):
    err_agent = Agent.objects.filter(identifier=ERR_IDENTIFIER)
    if not err_agent:
        err_agent = Agent.create(identifier=ERR_IDENTIFIER)
        err_agent.remote_ip = '127.0.0.1'
        err_agent.operating_system = 'Windows'
        err_agent.computer_name = 'Err-PC'
        err_agent.username = 'Err-Agent'
        err_agent.protocol = 'http'
        err_agent.save()
    else:
        err_agent = Agent.objects.get(identifier=ERR_IDENTIFIER)

    err_output = Output()
    err_output.agent = err_agent
    err_output.session_id = session_id
    err_output.output = err
    err_output.save()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class PipelineError(Exception):
    pass


class Pipeline(object):
    MODULE_LIST = ['nmap']

    def __init__(self):
        self.modules_loaded = {}
        self.agent_id_list = []
        self.session_id = 0

    def create_session(self, agent_id_list):
        session = Session()
        session.save()

        for agent_identifier in agent_id_list:
            agent = Agent.objects.filter(identifier=agent_identifier)[0]
            agent_session = Agent_session()
            agent_session.agent = agent
            agent_session.session = session
            agent_session.save()

        self.agent_id_list = agent_id_list
        self.session_id = session.id
        store_data(self.modules_loaded, self.session_id)

        return session.id

    def load_session(self, session_id):
        agent_sessions = Agent_session.objects.filter(session_id=session_id)

        agent_id_list = []
        for agent_session in agent_sessions:
            agent_id_list.append(agent_session.agent.identifier)

        self.agent_id_list = agent_id_list
        self.session_id = session_id
        self.modules_loaded = load_data(self.session_id)

        return agent_id_list

    def destroy_session(self, session_id):
        Session.objects.filter(session_id=session_id).delete()
        self.agent_id_list = []

    def load_module(self, module_name):
        if module_name in self.MODULE_LIST:
            if module_name in self.modules_loaded:
                raise PipelineError('Module already loaded!')

            # initialise the module
            mod_class = getattr(module_class, module_name)
            mod_instance = mod_class(agent_id_list=self.agent_id_list)

            self.modules_loaded[module_name] = mod_instance
            store_data(self.modules_loaded, self.session_id)

    def module_handler(self, module, commandline):
        if module == 'nmap':
            workloads = self.modules_loaded[module].parse_command(commandline)
            for agent_id in workloads:
                self.run_individual(agent_id, workloads[agent_id])

    def run_individual(self, agent_id, commandline):
        Agent.objects.get(identifier=agent_id).push_cmd(commandline, self.session_id)

    def run(self, commandline):
        command_list = commandline.split()
        command = command_list[0]

        try:
            # run a loaded module
            if command in self.MODULE_LIST:
                if command in self.modules_loaded:
                    self.module_handler(command, commandline)
                else:
                    raise PipelineError('Please load module <{}> first'.format(command))

            # load a new module
            elif command == 'load' and len(command_list) == 2 and command_list[1] in self.MODULE_LIST:
                self.load_module(command_list[1])
                raise Exception('Module <{}> loaded'.format(command_list[1]))

            # run in a normal cmdline
            else:
                for agent_id in self.agent_id_list:
                    self.run_individual(agent_id, commandline)

        except BaseException as err:
            output_error(err, self.session_id)

