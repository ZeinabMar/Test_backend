from scapy.all import sniff
import struct
from datetime import datetime
import binascii
import socket



sock_created = False
sniffer_socket = 0

def analyze_ether_header(data_recv):
    ip_bool = False

    eth_hdr = struct.unpack('!6s6sH', data_recv[:14])
    dest_mac = binascii.hexlify(eth_hdr[0])
    src_mac = binascii.hexlify(eth_hdr[1])
    proto = eth_hdr[2] >> 8
    data = data_recv[14:]
    assert dest_mac != [0,0,0,0,0,0,0,0,0,0,0,0]
    assert src_mac != [0,0,0,0,0,0,0,0,0,0,0,0]
    if proto != 8 :
        print("Destination MAC: %s:%s:%s:%s:%s:%s " % (dest_mac[0:2], dest_mac[2:4], dest_mac[4:6], dest_mac[6:8], dest_mac[8:10], dest_mac[10:12]))
        print("Source MAC: %s:%s:%s:%s:%s:%s " % (src_mac[0:2], src_mac[2:4], src_mac[4:6], src_mac[6:8], src_mac[8:10], src_mac[10:12]))
        print("PROTOCOL: %hu" % proto)
        if proto == 0x08:
            ip_bool = True        
        print("recieving is ok")

    return data, ip_bool

# Dictionary to store MAC addresses and last update times

mac_last_update = {}

from datetime import timedelta



max_elapsed_time = timedelta(seconds=10)  # Example maximum elapsed time



def update_elapsed_time():

    global mac_last_update, max_elapsed_time

    current_time = datetime.now()

    for mac, last_update_time in mac_last_update.items():

        elapsed_time = current_time - last_update_time

        if elapsed_time > max_elapsed_time:

            print(f"MAC: {mac}, Elapsed time: {elapsed_time}")









def packet_callback(packet):

    global mac_last_update



    if packet.haslayer('IP') and packet.haslayer('Ether') and packet['IP'].dport == 50001:

        mac = packet['Ether'].src

        current_time = datetime.now()



        # Check if MAC address is not in the dictionary

        if mac not in mac_last_update:

            mac_last_update[mac] = current_time

            print(f"New MAC address {mac} added at {current_time}")

        else:

            # Update the last update time for existing MAC address

            mac_last_update[mac] = current_time



        #print("Source IP:", packet['IP'].src)

        #print("Source MAC:", mac)

        #print("Payload:", packet['TCP'].payload)

        print(".", end='', flush=True)

        update_elapsed_time()


def main():
    global sock_created
    global sniffer_socket

    print("Sniffer Running...\n")
    if sock_created == False:
        while True:
            sniffer_socket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
            sock_created = True

            # data_recv_form = sniffer_socket.recvfrom(2048)
            data_recv = sniffer_socket.recv(2048)

            # print(data_recv_form)    

            data_recv, ip_bool = analyze_ether_header(data_recv)
    # sniff(prn=packet_callback, filter='tcp port 50001', store=False)



if __name__ == "__main__":

    main()

