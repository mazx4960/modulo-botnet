from django.views.decorators.http import require_POST
from django.shortcuts import redirect, reverse, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from ..api.models import Agent, Session
from ..api.utils import Pipeline


@login_required(login_url="accounts:login")
def dashboard(request):
    compromised_agents = Agent.objects.all()
    return render(request, 'webui/dashboard.html', {'agents':compromised_agents})


@login_required
def agent_list(request):
    pass


@login_required
def agent_detail(request):
    pass


# @login_required(login_url="accounts:login")
# @require_POST
# def create_session(request):
#     session_id = 0
#
#     if request.method == "POST":
#         selected_agent_list = request.POST.getlist("selected_bots[]")
#         return render(request, 'webui/session.html', {'selected_bots': selected_agent_list, 'session_id': session_id})

@login_required(login_url="accounts:login")
@require_POST
def create_session(request):
    agent_id_list = request.POST.getlist('selected_bots[]')
    # session_id = 1
    session_id = Pipeline().create_session(agent_id_list)
    return render(request, 'webui/session.html', {'selected_bots': agent_id_list, 'session_id': session_id})


@login_required(login_url="accounts:login")
def view_session(request, session_id):
    pass


def refresh_terminal(request):
    """
    Function to handle refresh requests from session page
    """
    if request.is_ajax():
        # Get data from db again
        session_id = request.POST.get('session_id')
        stored_sessions = Session.objects.all()
        for session in stored_sessions:
            if str(session.id) == session_id:
                return JsonResponse({'session_output': str(session.session_dump)})
