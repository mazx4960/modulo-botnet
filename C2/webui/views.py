from django.views.decorators.http import require_POST
from django.shortcuts import redirect, reverse, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from api.models import Agent


@login_required(login_url="accounts:login")
def index(request):
    return render(request, 'webui/index.html')


@login_required(login_url="accounts:login")
def dashboard(request):
    compromised_agents = Agent.objects.all()
    return render(request, 'webui/dashboard.html', {'agents':compromised_agents})


@login_required(login_url="accounts:login")
def testfunc(request):
    return render(request, 'webui/test.html')


@login_required
def agent_list(request):
    pass


@login_required
def agent_detail(request):
    pass


@require_POST
def create_session(request):
    session_id = 0
    return redirect(reverse('webui:session', kwargs={'session_id': session_id}))


@login_required
def view_session(request, session_id):
    pass
