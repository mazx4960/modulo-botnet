from django.urls import path
from . import views


urlpatterns = [
    path('<int:agent_identifier>/push/', views.push_command, name='push_command'),
    path('<int:agent_identifier>/get/', views.get_command, name='get_command'),
    path('<int:agent_identifier>/output/', views.output_command, name='output_command')
]