from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def get_command(request, agent_identifier):
    pass


@api_view(['POST'])
def output_command(request, agent_identifier):
    pass
