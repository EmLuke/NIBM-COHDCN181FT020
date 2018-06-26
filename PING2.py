import socket
import struct
from ctypes import *
import argparse


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


def ipv4_pack():

    parser = argparse.ArgumentParser()
    parser.add_argument('ip')
    args = parser.parse_args()

    dst = args.ip
    src = '192.168.8.103'

    ip_vhl = 5
    ip_ver = 4
    ip_ver = (ip_ver << 4) + ip_vhl

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

    ip_ttl = 255

    ip_proto = socket.IPPROTO_ICMP

    ip_chk = 0

    ip_saddr = socket.inet_aton(src)

    ip_daddr = socket.inet_aton(dst)

    ip_header = struct.pack('!BBHHHBBH4s4s',
                            ip_ver, ip_tos, ip_tol, ip_idf, ip_flg, ip_ttl, ip_proto, ip_chk, ip_saddr, ip_daddr)

    return src, dst, ip_header


try:
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    sniffer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))

except:
    print('socket not created')

(src, dst, ip_header) = ipv4_pack()
for i in range(4):
    sniffer.sendto(ip_header, (dst, 0))
    data = sock.recv(1024)
    ip = ip_h(data[14:])
    print("Reply From " + ip.dst_address + ": " + "TTL=" + ip.TTL)
