from inspect import isclass
from . import modules


class PipelineError(Exception):
    pass


class Pipeline(object):
    def __init__(self, agent_identifier_list):
        self.modules_loaded = []
        self.agent_identifier_list = agent_identifier_list

    def load_module(module_name):
        if module_name in dir(modules) and isclass(getattr(modules, module_name)):
            # initialise the module
            mod_instance = getattr(modules, module_name)
            mod_instance.initialise()

            if module_name in self.modules_loaded:
                raise PipelineError('Module already loaded!')
            self.modules_loaded[module_name] = mod_instance
    

