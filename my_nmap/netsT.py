import socket

class NetST:

    def __init__(self, dst_ips, dst_ports):
        self._dst_ips = dst_ips
        self._dst_ports = dst_ports
        self._open_ports = {}

    def discover(self):
        for dst_ip in self._dst_ips:
            for dst_port in self._dst_ports:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    try:
                        s.connect((dst_ip, dst_port))
                        self._open_ports[dst_ip + ':' + str(dst_port)] = 'Open'
                    except ConnectionRefusedError:
                        self._open_ports[dst_ip + ':' + str(dst_port)] = 'Closed'
                    except TimeoutError:
                        self._open_ports[dst_ip + ':' + str(dst_port)] = 'Filtered'
        return self._open_ports

# For testing purposes

# if __name__ == '__main__':
#     test = NetST(['192.168.2.178', '192.168.2.200'], [80, 4000])
#     # test = NetST(['192.168.2.253'], [80, 4000])
#     print(test.discover())
