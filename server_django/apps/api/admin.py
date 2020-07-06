from django.contrib import admin
from .models import Agent, Command, Session, Agent_session, Output


# Register your models here.
admin.site.register(Agent)
admin.site.register(Command)
admin.site.register(Session)
admin.site.register(Agent_session)
admin.site.register(Output)
