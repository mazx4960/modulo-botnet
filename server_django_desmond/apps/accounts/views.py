from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            # login user
            requested_user = login_form.get_user()
            login(request, requested_user)
            return redirect('webui:dashboard')
    else:
        login_form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'login_form':login_form})


@login_required(login_url="accounts:login")
def logout_view(request):
    logout(request)
    return redirect('accounts:login')
