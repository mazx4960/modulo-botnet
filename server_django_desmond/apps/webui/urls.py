from django.urls import path

from . import views

app_name = 'webui'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('agents/', views.agent_list, name='agent_list'),
    path('agent_terminal/<int:agent_id>/', views.agent_detail, name='agent_detail'),
    path('create_session/', views.create_session, name='create_session'),
    path('refresh_terminal/', views.refresh_terminal, name='refresh_terminal'),
    path('session/<int:session_id>/', views.view_session, name='view_session'),
]