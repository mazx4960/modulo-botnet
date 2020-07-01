from django.urls import path

from . import views

app_name = 'webui'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('test', views.testfunc, name='test'),
    path('agents/', views.agent_list, name='agent_list'),
    path('agent_terminal/<int:agent_id>/', views.agent_detail, name='agent_detail'),
    path('create_session/', views.create_session, name='create_session'),
    path('session/<int:session_id>/', views.view_session, name='view_session'),
]