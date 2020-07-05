from scapy.all import *
import random

conf.verb = 0


class HostPS:

    def __init__(self, src_ip, dst_ips, dst_ports):
        self._src_ip = src_ip
        self._dst_ips = dst_ips
        self._dst_ports = dst_ports
        self._hosts = []

    def discover(self):
        for dst_ip in self._dst_ips:
            for dst_port in self._dst_ports:
                src_port = random.randint(1024, 65535)
                ip = IP(src=self._src_ip, dst=dst_ip)
                syn = TCP(sport=src_port, dport=dst_port, flags='S', seq=1000)

                synack = sr1(ip / syn, timeout=0.1)
                if synack != None:
                    self._hosts.append(dst_ip)
                    if synack[TCP].flags == 'SA':
                        ack = TCP(sport=src_port, dport=dst_port, flags='R', seq=synack[TCP].ack+1,
                                  ack=synack[TCP].seq+1)
                        send(ip / ack)
                    break
        return self._hosts

# For testing purposes

# if __name__ == '__main__':
#     test = HostPS('192.168.2.119', ['192.168.2.178'], [80, 4000])
#     # test = HostPS('192.168.2.119', ['192.168.2.253'], [80, 4000])
#     print(test.discover())
