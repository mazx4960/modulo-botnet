from django.views.decorators.http import require_POST
from django.shortcuts import redirect, reverse, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from ..api.models import Agent, Session, Output
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


@login_required(login_url="accounts:login")
@require_POST
def create_session(request):
    """
    Initialise the session and redirects the webpage to the view session page

    :param request:
    :return:
    """
    agent_id_list = request.POST.getlist('selected_bots[]')
    session_id = Pipeline().create_session(agent_id_list)
    return redirect(reverse('webui:view_session', args=(session_id, )))


@login_required(login_url="accounts:login")
def view_session(request, session_id):
    """
    Returns the view session page which dynamically refresh the agents output

    :param request:
    :param session_id:
    :return:
    """
    agent_id_list = Pipeline().load_session(session_id)
    return render(request, 'webui/session.html', {'selected_bots': agent_id_list, 'session_id': session_id})


def refresh_terminal(request):
    """
    Function to handle refresh requests from session page
    """
    if request.is_ajax():
        # Get data from db again
        session_id = request.POST.get('session_id')
        session_outputs = Output.objects.filter(session_id=session_id)

        full_output = ''
        for session_output in session_outputs:
            output = '\nAgent: <{}>\n{}\n{}\n'.format(session_output.agent.identifier, '='*20, session_output.output)
            full_output += output

        return JsonResponse({'session_output': full_output})
