import sys
import hostPR
import hostPS
import netsS
import netsU
import netsA
import netsT
import ipaddress
import os
from scapy.all import *

ERROR_MSG = """
Usage: python mainframe.py [Scan type] {Targets} [Ports]
(Example: python mainframe.py -sT 10.0.0.0-10.255.255.255 1-65535)
SCAN TYPE - HOST DISCOVERY
-PR: Arp ping
-PS: Syn scan

SCAN TYPE -  SCAN TECHNIQUES
-sS: TCP SYN port scan (Default)
-sT: TCP connect port scan
-sU: UDP port scan
-sA: TCP ACK port scan

SCAN TYPE - Additional Module
-OT <python file>

TARGETS
10.0.0.0
10.0.0.0-10.255.255.255
10.0.0.0/8
Can use both methods

PORTS
80: Only 1 port
1-65535: All ports
80,4000,5000: Selected ports
"""

SCAN_TYPE = ['-PR', '-PS', '-sS', '-sT', '-sU', '-sA', '-OT']

def main():
    if len(sys.argv) < 2:
        print(ERROR_MSG)
        return
    if sys.argv[1] not in SCAN_TYPE:
        scan_type = '-sS'
        ptr = 1
    else:
        scan_type = sys.argv[1]
        ptr = 2
    if scan_type == '-OT':
        if os.path.isfile(sys.argv[ptr]):
            new_file = sys.argv[ptr]
            a = exec(open(new_file).read())
        else:
            print(ERROR_MSG)
            return
    else:
        ip_lst = []
        if '/' in sys.argv[ptr]:                           # Get list of IP addresses
            ip_sub_lst = list(ipaddress.ip_network(sys.argv[ptr]).hosts())
            for ip in ip_sub_lst:
                ip_lst.append(str(ip))
        elif '-' in sys.argv[ptr]:
            [min_ip, max_ip] = sys.argv[ptr].split('-')
            min_ip = ipaddress.ip_address(min_ip)
            max_ip = ipaddress.ip_address(max_ip)
            while min_ip <= max_ip:
                ip_lst.append(str(min_ip))
                min_ip += 1
        else:
            try:
                ip_lst = [str(ipaddress.ip_address(sys.argv[ptr]))]
            except ValueError:
                print(ERROR_MSG)
                return
        ptr += 1
        port_lst = []
        if '-' in sys.argv[ptr]:                            # Get list of ports
            [min_port, max_port] = sys.argv[ptr].split('-')
            min_port = int(min_port)
            max_port = int(max_port)
            if min_port in range(1, 65536) and max_port in range(1, 65536) and min_port <= max_port:
                while min_port <= max_port:
                    port_lst.append(min_port)
                    min_port += 1
            else:
                print(ERROR_MSG)
                return
        elif sys.argv[ptr].isdigit():
            port_lst = [int(sys.argv[ptr])]
        else:
            port_lst = sys.argv[ptr].split(',')
            for pos in range(len(port_lst)):
                port_lst[pos] = int(port_lst[pos])
        src_ip = IP().src

        if scan_type == '-PR':
            results = hostPR.HostPR(ip_lst)
            print(results.discover())
        elif scan_type == '-PS':
            results = hostPS.HostPS(src_ip, ip_lst, port_lst)
            print(results.discover())
        elif scan_type == '-sS':
            results = netsS.NetSS(src_ip, ip_lst, port_lst)
            print(results.discover())
        elif scan_type == '-sT':
            results = netsT.NetST(ip_lst, port_lst)
            print(results.discover())
        elif scan_type == '-sU':
            results = netsU.NetSU(src_ip, ip_lst, port_lst)
            print(results.discover())
        elif scan_type == '-sA':
            results = netsA.NetSA(src_ip, ip_lst, port_lst)
            print(results.discover())
    return



if __name__ == '__main__':
    main()