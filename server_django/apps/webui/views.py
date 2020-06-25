from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


# @login_required
def index(request):
    return render(request, 'webui/index.html')


@login_required
def agent_list(request):
    pass


@login_required
def agent_detail(request):
    pass


@login_required
def view_session(request):
    pass
