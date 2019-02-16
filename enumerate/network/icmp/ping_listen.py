#!/usr/bin/env python3
import socket, struct

PACKET_ID = 45821 # must match send

s = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)
try:
    s.setsockopt(socket.SOL_IP, socket.IP_HDRINCL, 1)
    while True:        
        data, addr = s.recvfrom(1024)
        typ, code, checksum, pid, sequence = struct.unpack("bbHHh", data[20:28])
        if typ != 8 and pid == PACKET_ID:
            print(addr[0])
except Exception as e:
    print('ERROR:', str(e))
finally:
    s.close()

# USAGE: sudo ./ping_listen.py
