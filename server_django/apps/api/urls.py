from django.urls import path
from . import views


urlpatterns = [
    path('<str:agent_identifier>/push', views.push_command, name='push_command'),
    path('<str:agent_identifier>/get', views.get_command, name='get_command'),
    path('<str:agent_identifier>/output', views.output_command, name='output_command')
]