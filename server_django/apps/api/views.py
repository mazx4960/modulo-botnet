from django.views.decorators.http import require_POST
from django.shortcuts import redirect

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .utils import Pipeline


@require_POST
def create_session(request):
    if request.method == "POST":
        pass
    return redirect(reverse('webui:index'))


@api_view(['POST'])
def get_command(request, agent_identifier):
    pass


@api_view(['POST'])
def output_command(request, agent_identifier):
    pass
