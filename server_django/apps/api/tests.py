import datetime

from django.test import TestCase

from .models import Agent, Command, User


class AgentModelTest(TestCase):
    def test_is_online_within_30_seconds(self):
        """
        is_online() returns true if the last login was within 30 seconds
        """
        time_10_secs_ago = datetime.datetime.now() - datetime.timedelta(seconds=10)
        agent_online_10_secs_ago = Agent(last_online=time_10_secs_ago)
        self.assertIs(agent_online_10_secs_ago.is_online(), True)

    def test_is_online_more_than_30_seconds(self):
        """
        is_online() returns False if the last login was more than 30 seconds ago
        """
        time_60_secs_ago = datetime.datetime.now() - datetime.timedelta(seconds=60)
        agent_online_60_secs_ago = Agent(last_online=time_60_secs_ago)
        self.assertIs(agent_online_60_secs_ago.is_online(), False)


class nmapTest(TestCase):
    pass

