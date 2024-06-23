#!/usr/bin/env python3

target_ip = "192.168.2.87"

import socket
import threading
import time

def send(s):
    while True:
        time.sleep(1)
        # packet = b'\x10\xaa\xaa\xaa\xaa\xaa\xaa'

        packet = b'\x08\x00\xf7\xff\x00\x00\x00\x00'
        print(">>>>>>> %s"%(packet))
        s.sendto(packet, (target_ip, 0))

def recv(s):
    while True:
        d = s.recvfrom(65534)
        if d[1][0] != target_ip:
            continue
        packet = d[0][20:]
        print("<<<<<<< %s"%(packet))

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    t1 = threading.Thread(target = recv, args=[s]).start()
    t2 = threading.Thread(target = send, args=[s]).start()

if __name__ == '__main__':
    main()