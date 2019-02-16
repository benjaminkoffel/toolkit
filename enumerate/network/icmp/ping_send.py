#!/usr/bin/env python3
import os, sys, socket, struct, time, ipaddress
import multiprocessing.dummy

PACKET_ID = 45821 # must match listen

ICMP_ECHO_REQUEST = 8

def checksum(source_string):
    sum = 0
    countTo = (len(source_string) / 2) * 2
    count = 0
    while count < countTo:
        thisVal = source_string[count + 1] * 256 + source_string[count]
        sum = sum + thisVal
        sum = sum & 0xffffffff
        count = count + 2
    if countTo < len(source_string):
        sum = sum + ord(source_string[len(source_string) - 1])
        sum = sum & 0xffffffff
    sum = (sum >> 16)  +  (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def ping(dest_addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    try:
        header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, 0, PACKET_ID, 1)
        data = struct.pack("d", time.time()) + ((192 - struct.calcsize("d")) * "Q").encode()
        check = checksum(header + data)
        header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(check), PACKET_ID, 1)
        packet = header + data
        s.sendto(packet, (dest_addr, 1))
    except Exception as e:
        print(e)
    finally:
        s.close()

hosts = [str(i) for r in sys.argv[3].split(',') for i in ipaddress.IPv4Network(r)] * int(sys.argv[1])
print('SENDING ICMP PING', len(hosts))
results = multiprocessing.dummy.Pool(int(sys.argv[2])).map(ping, hosts)

# USAGE: sudo ./ping_send.py 3 128 192.168.1.0/24 
