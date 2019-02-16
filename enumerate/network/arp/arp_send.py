#!/usr/bin/env python3
import binascii, ipaddress, multiprocessing.dummy, os, socket, struct, sys, time

def arp(dest_addr):
    mac_addr = binascii.unhexlify(sys.argv[5].replace(':', ''))
    src_addr = socket.gethostbyname(socket.gethostname())
    eth_hdr = struct.pack("!6s6s2s", b'\xff\xff\xff\xff\xff\xff', mac_addr, b'\x08\x06')             
    arp_hdr = struct.pack("!2s2s1s1s2s", b'\x00\x01', b'\x08\x00', b'\x06', b'\x04', b'\x00\x01')          
    arp_src = struct.pack("!6s4s", mac_addr, socket.inet_aton(src_addr))
    arp_dst = struct.pack("!6s4s", b'\x00\x00\x00\x00\x00\x00', socket.inet_aton(dest_addr))
    s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0806))
    s.bind((sys.argv[4], socket.htons(0x0806)))
    s.send(eth_hdr + arp_hdr + arp_src + arp_dst)

hosts = [str(i) for r in sys.argv[3].split(',') for i in ipaddress.IPv4Network(r)] * int(sys.argv[1])
print('SENDING ARP FRAME', len(hosts))
results = multiprocessing.dummy.Pool(int(sys.argv[2])).map(arp, hosts)

# USAGE: sudo ./arp_send.py 3 128 192.168.1.0/24 enp0s3 08:00:27:98:9f:c6
