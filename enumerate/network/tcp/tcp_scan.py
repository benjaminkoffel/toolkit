#!/usr/bin/env python3
import ipaddress
import multiprocessing.dummy
import socket
import sys

def tcp(host, port, connect_timeout, send_timeout):
    status = 'CLS'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(connect_timeout)
        s.connect((host, port))
        status = 'CON'
        s.settimeout(send_timeout)
        s.send(b'fDe2')
        status = 'SND'
        s.recv(8)
        status = 'RCV'
    except socket.error as e:
        pass
    finally:
        s.close()
    return host, port, status

default_ports = range(1, 65535)

ports = [int(i) for i in sys.argv[2].split(',')] if len(sys.argv) > 2 else default_ports

if sys.argv[1].startswith('.'):
    with open(sys.argv[1]) as f:
        ranges = [line.strip() for line in f.readlines() if line.strip()]
else:
    ranges = sys.argv[1].split(',')

ips = [str(i) for r in ranges for i in ipaddress.IPv4Network(r)]

params = [(i, p, 0.1, 0.1) for i in ips for p in ports]

pool = multiprocessing.dummy.Pool(128)

results = pool.starmap(tcp, params)

hosts = {}

for ip, port, status in results:
    if ip not in hosts:
        hosts[ip] = {}
    hosts[ip][port] = status

for ip, scan in hosts.items():
    print(ip, ' '.join('{}/{}'.format(p, s) for p, s in scan.items() if s in ['SND', 'RCV']))

# USAGE: ./tcp_scan.py 192.168.1.4
# USAGE: ./tcp_scan.py 192.168.1.0/24,192.168.2.0/24 80,443
# USAGE: ./tcp_scan.py ./file.txt 80,443
