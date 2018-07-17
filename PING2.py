import socket
import struct
from ctypes import *
import argparse
import sys
import time


class ip_h(Structure):

    _fields_ = [
        ("version", c_ubyte, 4),
        ("ihl", c_ubyte, 4),
        ("tos", c_ubyte),
        ("len", c_ushort),
        ("id", c_ushort),
        ("offset", c_ushort),
        ("ttl", c_ubyte),
        ("proto", c_ubyte),
        ("checksum", c_ushort),
        ("src", c_uint32),
        ("dst", c_uint32),
    ]

    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):

        self.TTL = str(self.ttl)

        self.src_address = socket.inet_ntoa(struct.pack("@I", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("@I", self.dst))


class ipv4_pack():

    parser = argparse.ArgumentParser()
    parser.add_argument('ip')
    args = parser.parse_args()

    dst = args.ip
    src = socket.gethostbyname(socket.getfqdn())
    ip_vhl = 5
    ip_ver = 4
    ip_vers = (ip_ver << 4) + ip_vhl

    ip_dsc = 0
    ip_ecn = 0
    ip_tos = (ip_dsc << 2) + ip_ecn

    ip_tol = 0

    ip_idf = 54321

    ip_rsv = 0
    ip_dtf = 0
    ip_mrf = 0
    ip_frag_offset = 0

    ip_flg = (ip_rsv << 7) + (ip_dtf << 6) + (ip_mrf << 5) + ip_frag_offset

    ip_ttl = 64

    ip_proto = 1

    ip_chk = 0

    ip_saddr = socket.inet_aton(src)

    ip_daddr = socket.inet_aton(socket.gethostbyname(dst))

    ip_header = struct.pack('!B B H H H B B H 4s 4s',
                            ip_vers, ip_tos, ip_tol, ip_idf, ip_flg, ip_ttl, ip_proto, ip_chk, ip_saddr, ip_daddr)


class icmp_packet():
    icmp_type = 8
    code = 0
    checksum = 0xf7ff
    identifier = 0
    sq_no = 0

    icmp_pack = struct.pack('!B B H H H', icmp_type, code, checksum, identifier, sq_no)

ipp = ipv4_pack()
icmp = icmp_packet()

class packet():
    pac = (ipp.ip_header + icmp.icmp_pack)

try:

    send_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    send_socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

except:
    print('socket not created')

pack = packet()
for i in range(4):
    time.sleep(1)
    send_socket.sendto(pack.pac, (ipp.dst, 0))
    data = recv_socket.recv(1024)
    ip = ip_h(data)
    print("Reply From " + ip.src_address + ": " + "TTL=" + ip.TTL)
