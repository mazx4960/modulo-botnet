from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def login(request):
    pass


def signup(request):
    pass


@login_required
def logout(request):
    pass