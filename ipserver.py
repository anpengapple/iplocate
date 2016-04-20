#!/usr/bin/env python
# coding: utf-8

import re
import socket
import sys
import time

HOST = 'localhost'
PORT = 9527
BUFFER = 256


def _time_it(func):
    def _deco(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)
        print 'running time:', time.time() - start
        return ret

    return _deco


class Ip2Addr(object):
    def __init__(self, filename):
        self.ips = list()
        self.save_ip_from_txt(filename)

    def save_ip_from_txt(self, filename):
        with open(filename, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break

                pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(.*)'
                info = re.match(pattern, line)
                if not info:
                    continue

                ip, _, addr = info.groups()
                ip = self._string2intip(ip)
                addr = addr.replace('CZ88.NET', '').strip()
                self.ips.append((ip, addr))

        print 'Saving Completed.'

    @_time_it
    def load_ip(self, ip):
        ret = self._find(self.ips, self._string2intip(ip))
        return self.ips[ret][1].decode('gbk').encode('utf-8')

    @staticmethod
    def _find(li, a):
        """
        二分法查找list中小于等于a的最大值的索引
        """
        l, r = 0, len(li) - 1
        if a < li[l][0] or a > li[r][0]:
            return -1

        m = (l + r) / 2
        while l < r:
            if li[m][0] <= a:
                l = m
                if li[m][0] == a or li[m + 1][0] > a:
                    return m
            else:
                r = m
                if li[m - 1][0] <= a:
                    return m - 1

            m = (l + r) / 2

    @staticmethod
    def _string2intip(s):
        """
        把一个字符串形式的ip地址转化为一个int值
        """
        ss = s.split('.')
        ip = 0
        for i in ss:
            ip = (ip << 8) + int(i)
        return ip

    @staticmethod
    def _intip2string(ip):
        """
        把一个int值形式的ip地址转化为一个字符串
        """
        a = (ip & 0xff000000) >> 24
        b = (ip & 0x00ff0000) >> 16
        c = (ip & 0x0000ff00) >> 8
        d = ip & 0x000000ff
        return "%d.%d.%d.%d" % (a, b, c, d)


def tcp_connection():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(0)

    ia = Ip2Addr(sys.argv[1])

    print "TCP Server started in %s: %s.\nIt can be stopped by CTRL-C" % (HOST, PORT)

    while True:
        client_sock, client_addr = sock.accept()

        try:
            client_sock.settimeout(5)
            ip = client_sock.recv(BUFFER).strip()

            client_sock.send(ia.load_ip(ip))
        except socket.timeout:
            print 'time out'
        finally:
            client_sock.close()

    sock.close()


def udp_connection():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind((HOST, PORT))

    ia = Ip2Addr(sys.argv[1])

    print "UDP Server started in %s: %s.\nIt can be stopped by CTRL-C" % (HOST, PORT)

    while True:
        ip, _ = udp_sock.recvfrom(BUFFER)
        udp_sock.sendto(ia.load_ip(ip), _)

    udp_sock.close()


if __name__ == '__main__':
    tcp_connection()
    # udp_connection()
