from scapy.all import *

conf.verb = 0


class HostPR:

    def __init__(self, dst_ips):
        self._dst_ips = dst_ips
        self._hosts = []

    def discover(self):
        for dst_ip in self._dst_ips:
            packet = arping(dst_ip)
            if packet[0]:
                self._hosts.append(dst_ip)
        return self._hosts

# For testing purposes

# if __name__ == '__main__':
#     test = HostPR(['192.168.2.178', '192.168.2.253'])
#     print(test.discover())
