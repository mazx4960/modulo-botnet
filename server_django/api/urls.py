from django.urls import include, path
from rest_framework import routers
from . import views


urlpatterns = [
    path('create_session/', views.create_session, name='create_session'),
    path('<int:agent_identifier>/get/', views.get_command, name='get_command'),
    path('<int:agent_identifier>/output/', views.output_command, name='output_command')
]