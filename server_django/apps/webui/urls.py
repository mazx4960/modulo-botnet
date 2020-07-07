from django.urls import path

from . import views

app_name = 'webui'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('agent_terminal/<str:agent_identifier>/', views.agent_terminal, name='agent_terminal'),
    path('create_session/', views.create_session, name='create_session'),
    path('session/<int:session_id>/', views.view_session, name='view_session'),
    path('refresh_terminal/', views.refresh_terminal, name='refresh_terminal'),
    path('send_instruction/', views.send_instruction, name='send_instruction'),
]