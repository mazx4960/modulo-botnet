# my_nmap
Is this how u do it lmao

## Pre-run
* Pip install scapy
* Download winpcap

## Explanation
* -PR: ARP discovery on local network
* -PS: TCP SYN discovery 
* -sS: TCP SYN port scan
* -sT: TCP connect port scan
* -sU: UDP port scan
* -sA: TCP ACK port scan
* -OT: Other additional modules


## Usage
For main function
```console
$ python mainframe.py <scantype> <hosts> <ports>
```
For other function
```console
$ python mainframe.py -OT <python file>
```
For help
```console
$ python mainframe.py 
```
An example (Go help to view more possible cases)
```console
$ python mainframe.py -sT 10.0.0.0-10.255.255.255 1-65535)
```

## Some extra helpful links
https://nmap.org/book/host-discovery-techniques.html

https://nmap.org/book/man-host-discovery.html

https://nmap.org/book/man-port-scanning-techniques.html
