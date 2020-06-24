from scapy.all import *
import random

conf.verb = 0


class NetSA:

    def __init__(self, src_ip, dst_ips, dst_ports):
        self._src_ip = src_ip
        self._dst_ips = dst_ips
        self._dst_ports = dst_ports
        self._open_ports = {}
        self._filtered_codes = [0, 1, 2, 9, 10, 13]

    def discover(self):
        for dst_ip in self._dst_ips:
            for dst_port in self._dst_ports:
                src_port = random.randint(1024, 65535)
                ip = IP(src=self._src_ip, dst=dst_ip)
                ack = TCP(sport=src_port, dport=dst_port, flags='A', seq=1000)

                reply = sr1(ip / ack, timeout=1)
                if reply is None or (reply.haslayer(ICMP) and reply[ICMP].code in self._filtered_codes):
                    self._open_ports[dst_ip + ':' + str(dst_port)] = 'Filtered'
                elif reply.haslayer(TCP) and reply[TCP].flags == 'R':
                    self._open_ports[dst_ip + ':' + str(dst_port)] = 'Unfiltered'
        return self._open_ports

# For testing purposes

# if __name__ == '__main__':
#     test = NetSA('192.168.2.120', ['192.168.2.178'], [80, 4000])
#     # test = NetSS('192.168.2.119', ['192.168.2.253'], [80, 4000])
#     print(test.discover())
