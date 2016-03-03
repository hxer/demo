# -*- coding: utf-8 -*-

"""
扫描周围无线网络，列出SSID and mac address

开启网卡监听模式(mon)，侦听无线网络流量
开启/关闭 监听模式
>sudo airmon-ng start/stop wlan0
找回网络管理图标
>NetworkManager start
"""

import sys

from scapy.all import *
from argparse import ArgumentParser


def packet_handler(pkt):
    ap_list = []

    if pkt.haslayer(Dot11):
        if pkt.type == 0 and pkt.subtype == 8:
            # filter mac address
            if pkt.addr2 not in ap_list:
                ap_list.append(pkt.addr2)
                print("Avaliable SSID: {name}, MAC: {addr}"
                      "".fomat(name=pkt.info, addr=pkt.addr2))

usage = "python {prog} <interface>\n".format(prog=sys.argv[0])
usage += "\te.g. python {prog} wlan0mon".format(prog=sys.argv[0])
parser = ArgumentParser(usage=usage)
parser.add_argument('interface', help="the interface needed to monitor")
args = parser.parse_args()

iface = args.interface
sniff(iface=iface, prn=packet_handler)
