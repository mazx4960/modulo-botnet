from . import module_class
from .models import Agent, Session, Agent_session


class PipelineError(Exception):
    pass


class Pipeline(object):
    MODULE_LIST = ['nmap']

    def __init__(self):
        self.modules_loaded = []
        self.agent_id_list = []

    def create_session(self, agent_id_list):
        session = Session()
        session.save()

        for agent_identifier in agent_id_list:
            agent = Agent.objects.get(identifier=agent_identifier)
            agent_session = Agent_session()
            agent_session.agent = agent
            agent_session.session = session
            agent_session.save()

        self.agent_id_list = agent_id_list

        return session.id

    def load_session(self, session_id):
        agent_sessions = Agent_session.objects.filter(session_id=session_id)

        agent_id_list = []
        for agent_session in agent_sessions:
            agent_id_list.append(agent_session.agent.identifier)

        self.agent_id_list = agent_id_list

    def destroy_session(self, session_id):
        Session.objects.filter(session_id=session_id).delete()
        self.agent_id_list = []

    def load_module(self, module_name):
        if module_name in self.MODULE_LIST:
            if module_name in self.modules_loaded:
                raise PipelineError('Module already loaded!')

            # initialise the module
            mod_instance = getattr(module_class, module_name)
            mod_instance.initialise(self.agent_id_list)

            self.modules_loaded[module_name] = mod_instance

    def module_handler(self, module, commandline):
        if module == 'nmap':
            workloads = self.modules_loaded[module].parse_command(commandline)
            for agent_id in workloads:
                self.run_individual(agent_id, workloads[agent_id])

    def run_individual(self, agent_id, commandline):
        Agent.objects.get(id=agent_id).push_cmd(commandline)

    def run(self, commandline):
        command = commandline.split()[0]
        if command in self.MODULE_LIST:
            self.module_handler(command, commandline)
        else:
            for agent_id in self.agent_id_list:
                self.run_individual(agent_id, commandline)

