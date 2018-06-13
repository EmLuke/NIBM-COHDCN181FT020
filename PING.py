from ctypes import *
import socket
import os
import struct


class ip_header(Structure):
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

        self.protocol_map = {1: "ICMP"}
        try:
            self.protocol = self.protocol_map[self.proto]
        except:
            self.protocol = str(self.proto)


class icmp_header(Structure):
    _fields_ = [
        ("type", c_ubyte),
        ("code", c_ubyte),
        ("checksum", c_ushort),
        ("unused", c_ushort),
        ("next_hop_mtu", c_ushort)
    ]

    def __new__(self, socket_buffer):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer):
        pass


conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x800))
conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

while True:
    data = conn.recvfrom(65565)[0]
    ip = ip_header(data[14:])

    if ip.protocol == "ICMP":
        print("Reply From " + ip.src_address + ": " + "TTL=" + ip.TTL)
