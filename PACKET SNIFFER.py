import socket
from ctypes import *
import struct
import binascii
import textwrap

TAB_1 = '\t - '
TAB_2 = '\t\t - '
TAB_3 = '\t\t\t - '
TAB_4 = '\t\t\t\t - '


class eth_header(Structure):

    _fields_ = [
        ("dst_mac", c_uint16 * 3),
        ("src_mac", c_uint16 * 3),
        ("eth_proto", c_ushort),
    ]

    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):

        self.dmac = binascii.hexlify(self.dst_mac)
        self.smac = binascii.hexlify(self.src_mac)
        socket.htons(self.eth_proto)


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

        self.version = 4
        self.ihl = 5
        self.vihl = self.version * self.ihl

        self.src_address = socket.inet_ntoa(struct.pack("@I", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("@I", self.dst))

        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
        try:
            self.protocol = self.protocol_map[self.proto]
        except:
            self.protocol = str(self.proto)


class tcp_header(Structure):
    _fields_ = [
        ("src", c_ushort),
        ("dst", c_ushort),
        ("sq_no", c_uint32),
        ("ack_no", c_uint32),
        ("offset", c_ubyte, 4),
        ("res", c_ubyte, 4),
        ("flags", c_ubyte),
        ("window", c_ushort),
        ("Tcheckcsum", c_ushort),
        ("pointer", c_ushort)
    ]


    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)


    def __init__(self, socket_buffer=None):

        self.src_port = socket.ntohs(self.src)
        self.dst_port = socket.ntohs(self.dst)

host = ''
sniffer = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))
#sniffer.bind((host, 0))

while True:

    data = sniffer.recvfrom(65535)[0]
    frame = eth_header(data[:14])
    print(TAB_1 + 'Ethernet Frame:')
    print(TAB_2 + 'Destination MAC: {}, Source MAC: {}, Type: {},'.format(frame.dmac, frame.smac, frame.eth_proto))

    ip = ip_header(data[14:])
    if frame.eth_proto == 8:

        print(TAB_1 + 'IPv4 Packet:')
        print(TAB_2 + 'Version: {}, Header Length: {},'.format(ip.version, ip.vihl))
        print(TAB_2 + 'Protocol: {}, Source: {}, Target: {}'.format(ip.protocol, ip.src_address, ip.dst_address))


        if ip.protocol == 'TCP':
            tcp = tcp_header(data[34:])
            print(TAB_1 + 'TCP Header:')
            print(TAB_2 + 'Source Port {}, Destination Port {},'.format(tcp.src_port, tcp.dst_port))

    print(TAB_1 + 'data: {},'.format(data[54:]))
    print("\n\n")
