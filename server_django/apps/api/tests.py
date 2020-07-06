from django.test import TestCase, Client
from django.utils import timezone

from .models import Agent
from .utils import Pipeline
from .module_class import nmap, nmapError

import datetime
from urllib.parse import urlencode
import json


class AgentModelTest(TestCase):
    def test_is_online_within_30_seconds(self):
        """
        is_online() returns true if the last login was within 30 seconds
        """
        time_10_secs_ago = timezone.now() - datetime.timedelta(seconds=10)
        agent_online_10_secs_ago = Agent(last_online=time_10_secs_ago)
        self.assertIs(agent_online_10_secs_ago.is_online(), True)

    def test_is_online_more_than_30_seconds(self):
        """
        is_online() returns False if the last login was more than 30 seconds ago
        """
        time_60_secs_ago = timezone.now() - datetime.timedelta(seconds=60)
        agent_online_60_secs_ago = Agent(last_online=time_60_secs_ago)
        self.assertIs(agent_online_60_secs_ago.is_online(), False)


class NmapTest(TestCase):
    def test_validate_command(self):
        """
        validate_command() would return a boolean depending on whether the nmap command is in the right format
        """
        nmap_test = nmap()

        # Test cases
        wrong_length_command = 'nmap'.split()
        invalid_option_command = 'nmap -A 192.168.1.1 10000'.split()
        bad_port_command = 'nmap -sS 192.168.1.1 100000'.split()
        valid_command_1 = 'nmap -sS 192.168.1.1/24 1-65535'.split()
        valid_command_2 = 'nmap -sS 192.168.1.1 1-65535'.split()
        valid_command_3 = 'nmap -sS 192.168.1.1/24 10000'.split()

        self.assertFalse(nmap_test.validate_command(wrong_length_command))
        self.assertFalse(nmap_test.validate_command(invalid_option_command))
        self.assertFalse(nmap_test.validate_command(bad_port_command))
        self.assertTrue(nmap_test.validate_command(valid_command_1))
        self.assertTrue(nmap_test.validate_command(valid_command_2))
        self.assertTrue(nmap_test.validate_command(valid_command_3))

    def test_gather_hosts_from_cidr(self):
        """
        gather_hosts_from_cidr() would return a list of ip addresses from a given cidr notation
        """
        nmap_test = nmap()

        # Test cases
        single_ip_addr = '192.168.1.1'
        multiple_ip_addr = '192.168.1.0/30'
        bad_cidr = '192.168.1.1,24'
        bad_cidr_2 = '24/192.168.1.1'
        bad_cidr_3 = '192.168.1/24'

        # Expected results
        single_ip_addr_expected = ['192.168.1.1']
        multiple_ip_addr_expected = ['192.168.1.0', '192.168.1.1', '192.168.1.2', '192.168.1.3']

        self.assertEqual(nmap_test.gather_hosts_from_cidr(single_ip_addr), single_ip_addr_expected)
        self.assertEqual(nmap_test.gather_hosts_from_cidr(multiple_ip_addr), multiple_ip_addr_expected)
        self.assertRaises(nmapError, nmap_test.gather_hosts_from_cidr, bad_cidr)
        self.assertRaises(nmapError, nmap_test.gather_hosts_from_cidr, bad_cidr_2)
        self.assertRaises(nmapError, nmap_test.gather_hosts_from_cidr, bad_cidr_3)

    def test_parse_commands(self):
        nmap_test = nmap()
        sample_agent_list = [1, 2, 3]
        nmap_test.initialise(sample_agent_list)

        # Test cases
        test_command = 'nmap -PS 192.168.1.1 1-10000'
        test_command_2 = 'nmap -PR 192.168.1.0/24 0'

        # Expected results
        test_command_expected = {
            1: 'nmap -PS 192.168.1.1 1-3334',
            2: 'nmap -PS 192.168.1.1 3334-6667',
            3: 'nmap -PS 192.168.1.1 6667-10000'
        }
        test_command_2_expected = {
            1: 'nmap -PR 192.168.1.0-192.168.1.85 0',
            2: 'nmap -PR 192.168.1.85-192.168.1.170 0',
            3: 'nmap -PR 192.168.1.170-192.168.1.255 0'
        }

        self.assertDictEqual(nmap_test.parse_command(test_command), test_command_expected)
        self.assertDictEqual(nmap_test.parse_command(test_command_2), test_command_2_expected)


class PipelineTest(TestCase):
    pass


class APITest(TestCase):
    TEST_IDENTIFIER = 'ffffffffffff'

    def setUp(self):
        self.client = Client()
        self.test_agent = Agent().create(self.TEST_IDENTIFIER)
        self.test_agent.remote_ip = '127.0.0.1'
        self.test_agent.operating_system = 'Windows'
        self.test_agent.computer_name = 'Test-PC'
        self.test_agent.username = 'Test-Agent'
        self.test_agent.protocol = 'http'
        self.test_agent.save()

        # Initialise the session
        self.session_id = Pipeline().create_session([self.TEST_IDENTIFIER])

    def test_push_command(self):
        sample_cmdline = {
            'cmdline': 'whoami',
            'session_id': 1,
        }

        # Send the post request
        response = self.client.post('/api/{}/push'.format(self.TEST_IDENTIFIER), urlencode(sample_cmdline),
                                    content_type='application/x-www-form-urlencoded')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check the response is an empty string
        self.assertEqual(response.content, b'""')

        # Check the cmdline field is inserted into the database
        commands = self.test_agent.commands.filter(cmdline=sample_cmdline['cmdline'])
        self.assertIsNotNone(commands)

    def test_get_command(self):
        agent_identifier = 'abcdefghijkl'
        sample_data = {
            'operating_system': 'Windows',
            'computer_name': 'Work-PC',
            'username': 'test_user'
        }

        # Send the post request
        response = self.client.post('/api/{}/get'.format(agent_identifier), urlencode(sample_data),
                                    content_type='application/x-www-form-urlencoded')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check the response is an empty string
        self.assertEqual(response.content, b'"{}"')

    def test_output_command(self):
        sample_output = {
            'output': 'Test-PC\Test-Agent'
        }

        # Send the post request
        response = self.client.post('/api/{}/{}/output'.format(self.TEST_IDENTIFIER, self.session_id),
                                    urlencode(sample_output), content_type='application/x-www-form-urlencoded')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check the response is an empty string
        self.assertEqual(response.content, b'""')

        # Check the cmdline field is inserted into the database
        self.test_agent.refresh_from_db()
        output = self.test_agent.outputs.order_by('-timestamp')[0].output
        self.assertIn(sample_output['output'], output)

    def test_push_then_get_command(self):
        agent_identifier = 'aaaaaaaaaaaa'

        sample_data = {
            'operating_system': 'Windows',
            'computer_name': 'Work-PC',
            'username': 'test_user_2'
        }

        # Send the post request to create the test user
        self.client.post('/api/{}/get'.format(agent_identifier), urlencode(sample_data),
                         content_type='application/x-www-form-urlencoded')

        # Initialise the session
        session_id = Pipeline().create_session([agent_identifier])
        sample_cmdline = {
            'cmdline': 'it works!',
            'session_id': session_id,
        }

        # Send the post request for push command
        self.client.post('/api/{}/push'.format(agent_identifier), urlencode(sample_cmdline),
                         content_type='application/x-www-form-urlencoded')

        # Send the post request to get the newly pushed command
        response = self.client.post('/api/{}/get'.format(agent_identifier,), urlencode(sample_data),
                                    content_type='application/x-www-form-urlencoded')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check the response is correct
        response_cmdline = json.loads(response.content.decode().strip('"').replace('\\', ''))
        self.assertDictEqual(response_cmdline, sample_cmdline)
