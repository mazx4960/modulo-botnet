from django.db import models
from django.utils import timezone


class Agent(models.Model):
    id = models.AutoField(primary_key=True)
    display_name = models.CharField(max_length=100)
    last_online = models.DateTimeField(default=timezone.now)
    remote_ip = models.GenericIPAddressField()
    operating_system = models.CharField(max_length=100)
    computer_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    identifier = models.CharField(max_length=20)  # the mac address of the computer
    protocol = models.CharField(max_length=50)  # dns or http
    # output = models.CharField(max_length=100000, default='')

    def __str__(self):
        return 'Agent <{}> ({})'.format(self.display_name, self.remote_ip)

    @classmethod
    def create(cls, identifier):
        return cls(display_name=identifier, identifier=identifier)

    def push_cmd(self, cmdline, session_id):
        command = Command()
        command.agent = self
        command.session_id = session_id
        command.cmdline = cmdline
        command.timestamp = timezone.now()
        command.save()

    def is_online(self):
        return (timezone.now() - self.last_online).seconds < 30


class Session(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Session <{}>'.format(self.id)


class Command(models.Model):
    id = models.AutoField(primary_key=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='commands')
    session_id = models.IntegerField()
    cmdline = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.cmdline


class Output(models.Model):
    id = models.AutoField(primary_key=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='outputs')
    session_id = models.IntegerField()
    output = models.TextField(max_length=100000, default='')
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Output <{}> from agent <{}> in session <{}>'.format(self.output[:10], self.agent.id,
                                                                    self.session_id)


class Agent_session(models.Model):
    id = models.AutoField(primary_key=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    def __str__(self):
        return 'Agent <{}> in session <{}>'.format(self.agent.id, self.session.id)
