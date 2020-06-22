from django.db import models
from datetime import datetime


class Agents(models.Model):
    id = models.AutoField(primary_key=True)
    display_name = models.CharField(max_length=100)
    last_online = models.DateTimeField()
    remote_ip = models.CharField(max_length=100)
    operating_system = models.CharField(max_length=100)
    computer_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)

    def __str__(self):
        return 'Agent <{}> ({})'.format(self.display_name, self.remote_ip)


class Commands(models.Model):
    id = models.AutoField(primary_key=True)
    agent = models.ForeignKey(Agents, on_delete=models.CASCADE)
    cmdline = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.cmdline


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=200)
    last_login = models.DateTimeField()
    last_login_ip = models.CharField(max_length=100)

    def __str__(self):
        return 'User <{}>'.format(self.username)
