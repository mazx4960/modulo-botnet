import re
import ipaddress


class nmapError(Exception):
    pass


class nmap(object):
    IPV4_RE = r'(\d{1,3}\.){3}\d{1,3}'
    CIDR_RE = r'^{}/[1-3]?[0-9]$'.format(IPV4_RE)

    OPTION = 1
    HOST = 2
    PORT = 3
    SCRIPT = 4

    def initialise(self, agent_list):
        """
        Initialise the module and ensure that all agents have nmap installed
        :param agent_list: a list of agent ids
        :return: None
        """
        self.agent_list = agent_list

    def validate_command(self, command_list):
        return True

    def parse_command(self, command):
        """
        Interpret the command in the string form and calls the respective functions
        Command format:
            nmap -sS 192.168.1.1/24 1-65535 --scripts=smileyface.py
            nmap -PS 192.168.1.1 1-10000
            nmap -PS 192.168.1.1-192.168.1.255 1-10000

        :param command: the command string to run
        :return: None
        """
        command_list = command.split()
        if not self.validate_command(command_list):
            raise nmapError('Invalid command!\n Usage: nmap options hosts [ports]')

        ip_list = self.gather_hosts_from_cidr(command_list[self.HOST])
        port_list = command_list[self.PORT].split('-')
        port_start, port_stop = int(port_list[0]), int(port_list[-1])
        workload = self.divide_workload(ip_list, port_start, port_stop, command_list)
        return workload

    def gather_hosts_from_cidr(self, cidr_string):
        if len(cidr_string.split('/')) == 1 and re.match(r'^{}$'.format(self.IPV4_RE), cidr_string):
            return [cidr_string]
        elif len(cidr_string.split('/')) == 2 and re.match(self.CIDR_RE, cidr_string):
            return [str(ip) for ip in ipaddress.IPv4Network(cidr_string)]
        else:
            raise nmapError('Invalid CIDR notation! Eg. 192.168.1.0/24')

    def divide_workload(self, ip_list, port_start, port_stop, command_list):
        """
        Divides the workload equally among the agents
        :param ip_list: a list of ip addresses
        :param port_start:
        :param port_stop:
        :param command_list: a list of the command bring split by groups
        :return: a dictionary of commands that would be ran on the individual agents
        """
        split_by_ip = False
        ips_per_agent = 0
        ports_per_agent = 0
        if command_list[self.OPTION] == '-PR':
            total_ips = len(ip_list)
            ips_per_agent = total_ips // len(self.agent_list)
            split_by_ip = True
        else:
            total_ports = port_stop - port_start + 1
            ports_per_agent = total_ports // len(self.agent_list)

        workload = {}
        for index in range(len(self.agent_list)):
            if split_by_ip:
                workload[self.agent_list[index]] = self.generate_agent_command(split_by_ip, index, ips_per_agent,
                                                                               command_list, ip_list=ip_list)
            else:
                workload[self.agent_list[index]] = self.generate_agent_command(split_by_ip, index, ports_per_agent,
                                                                               command_list, port_start=port_start,
                                                                               port_stop=port_stop)
        return workload

    def generate_agent_command(self, split_by_ip, index, no_per_agent, command_list, ip_list=None, port_start=None,
                               port_stop=None):
        if split_by_ip:
            start = index * no_per_agent
            end = ((index + 1) * no_per_agent) if ((index + 1) * no_per_agent) < len(ip_list) else -1
            command_list[self.HOST] = '{}-{}'.format(ip_list[start], ip_list[end])
            return ' '.join(command_list)
        else:
            start = port_start + (index * no_per_agent)
            end = (port_start + (index + 1) * no_per_agent) if ((index + 1) * no_per_agent) < (
                    port_stop - port_start) else port_stop
            command_list[self.PORT] = '{}-{}'.format(start, end)
            return ' '.join(command_list)


class dns_tunneling(object):
    def initialise(self):
        pass
