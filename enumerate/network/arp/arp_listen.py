#!/usr/bin/env python3
import binascii, socket, struct

s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
try:
    while True:
        packet = s.recvfrom(2048)
        ethernet_header = packet[0][0:14]
        ethernet_detailed = struct.unpack('!6s6s2s', ethernet_header)
        arp_header = packet[0][14:42]
        arp_detailed = struct.unpack('2s2s1s1s2s6s4s6s4s', arp_header)
        if ethernet_detailed[2] != b'\x08\x06': continue # skip non-ARP packets
        if ethernet_detailed[0] == b'\xff\xff\xff\xff\xff\xff': continue # skip not found
        # data = {
        #     'eth_dest_mac': binascii.hexlify(ethernet_detailed[0]),
        #     'eth_source_mac': binascii.hexlify(ethernet_detailed[1]),
        #     'eth_type': binascii.hexlify(ethernet_detailed[2]),
        #     'arp_hardware_type': binascii.hexlify(arp_detailed[0]),
        #     'arp_protocol_type': binascii.hexlify(arp_detailed[1]),
        #     'arp_hardware_size': binascii.hexlify(arp_detailed[2]),
        #     'arp_protocol_size': binascii.hexlify(arp_detailed[3]),
        #     'arp_op_code': binascii.hexlify(arp_detailed[4]),
        #     'arp_source_mac': binascii.hexlify(arp_detailed[5]),
        #     'arp_source_ip': socket.inet_ntoa(arp_detailed[6]),
        #     'arp_dest_mac': binascii.hexlify(arp_detailed[7]),
        #     'arp_dest_ip': socket.inet_ntoa(arp_detailed[8])
        # }
        print(socket.inet_ntoa(arp_detailed[6]))
except Exception as e:
    print('ERROR:', str(e))
finally:
    s.close()

# USAGE: sudo ./arp_listen.py
