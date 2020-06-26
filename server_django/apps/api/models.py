from django.db import models
from datetime import datetime


class Agent(models.Model):
    id = models.AutoField(primary_key=True)
    display_name = models.CharField(max_length=100)
    last_online = models.DateTimeField(default=datetime.now)
    remote_ip = models.GenericIPAddressField()
    operating_system = models.CharField(max_length=100)
    computer_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    identifier = models.CharField(max_length=20) # the mac address of the computer

    def __str__(self):
        return 'Agent <{}> ({})'.format(self.display_name, self.remote_ip)

    @classmethod
    def create(cls, identifier):
        return cls(display_name=identifier, identifier=identifier)

    def push_cmd(self, cmdline):
        command = Command()
        command.agent = self
        command.cmdline = cmdline
        command.timestamp = datetime.now()
        command.save()

    def is_online(self):
        return (datetime.now() - self.last_online).seconds < 30


class Command(models.Model):
    id = models.AutoField(primary_key=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='commands')
    cmdline = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.cmdline


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=200)
    last_login = models.DateTimeField(default=datetime.now)
    last_login_ip = models.GenericIPAddressField()

    def __str__(self):
        return 'User <{}>'.format(self.username)


class Session(models.Model):
    id = models.AutoField(primary_key=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return 'Session <{}>'.format(self.id)


class Agent_session(models.Model):
    id = models.AutoField(primary_key=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    protocol = models.CharField(max_length=50)

    def __str__(self):
        return 'Agent <{}> in session <{}>'.format(self.agent.id, self.session.id)
