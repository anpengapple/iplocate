#!/usr/bin/env python
# coding: utf-8

import socket
import sys

HOST = 'localhost'
PORT = 9527
BUFFER = 256


def tcp_ip2address(ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.send(ip)
    addr = sock.recv(BUFFER)
    sock.close()

    return addr


def udp_ip2address(ip):
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.sendto(ip, (HOST, PORT))
    addr, _ = udp_sock.recvfrom(BUFFER)
    udp_sock.close()

    return addr

if __name__ == '__main__':
    print tcp_ip2address(sys.argv[1])
    # print udp_ip2address(sys.argv[1])
