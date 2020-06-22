from django.urls import include, path
from rest_framework import routers
from . import views


urlpatterns = [
    path('<int:agent_identifier>/get/', views.get_command),
    path('<int:agent_identifier>/output/', views.output_command)
]