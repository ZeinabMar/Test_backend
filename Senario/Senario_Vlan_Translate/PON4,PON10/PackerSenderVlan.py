from scapy.all import Ether, IP, TCP, sendp, sniff, Raw, ICMP
import threading 
import socket
import struct
import time
import binascii


selectedPort=50001

dst_ip='192.168.2.87'

vlan_id=700

dst_mac='10:c3:7b:91:39:f8'


#packet = Ether(src='00:11:22:33:44:55', dst='08:00:27:74:bc:d6') / IP(dst=dst_ip) / #TCP(dport=selectedPort)

    # Adding Dot1Q layer with VLAN ID 700

#packet = Ether(src=src_mac, dst=dst_mac) / \

#     Dot1Q(vlan=vlan_id) / \

#     IP(dst=dst_ip) / \

#     TCP(dport=selectedPort) / \

#     payload



selectedInterface="ens38"





def read_mac_addresses(file_path):

    with open(file_path, 'r') as file:

        mac_addresses = [line.strip() for line in file if line.strip()]

    return mac_addresses



def send_packet(src_mac_address,pay_load):

    # Craft an Ethernet frame with the desired source and destination MAC addresses
    custom_payload = b'\xaa' * 2
    ip_pkt = IP(dst=dst_ip, ttl=255, proto=254)
    ether_pkt = Ether(src=src_mac_address)
    packet = ether_pkt / ip_pkt / Raw(load=custom_payload)/ ICMP()
    print(src_mac_address) 

    # Send the packet

    sendp(packet, iface=selectedInterface, verbose=False)

def receive_ping(source_ip, timeout=4):
    # Function to receive ICMP echo replies
    def icmp_reply(pkt):
        print(f"in is pkt:  {pkt}")
        if ICMP in pkt and pkt[IP].src == source_ip:
            print(f"Received ICMP reply from {pkt[IP].src}")
            return True
        return False

    # Sniff for ICMP replies
    print("ICPM REPLY BEGIN")
    sniff(filter="icmp", prn=icmp_reply, timeout=timeout)

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
    print("Destination MAC: %s:%s:%s:%s:%s:%s " % (dest_mac[0:2], dest_mac[2:4], dest_mac[4:6], dest_mac[6:8], dest_mac[8:10], dest_mac[10:12]))
    print("Source MAC: %s:%s:%s:%s:%s:%s " % (src_mac[0:2], src_mac[2:4], src_mac[4:6], src_mac[6:8], src_mac[8:10], src_mac[10:12]))
    print("PROTOCOL: %hu" % proto)
    if proto == 0x08:
        ip_bool = True        
    print("recieving is ok")

    return data, ip_bool

def recv(s):
    while True:
        d = s.recvfrom(65534)
        if d[1][0] != dst_ip:
            continue
        packet = d[0][20:]
        print("< %s"%(packet))

def main():

    mac_addresses = read_mac_addresses('/home/zeinab/test_sp5100/test_sp5100_rest/Senario/Senario_Vlan_Translate/PON4,PON10/mac.txt')
    while True:

        for src_mac in mac_addresses:

            payload = "Hello, world!"

            send_packet(src_mac, payload)
            time.sleep(0.1)
            icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            print(icmp_socket)
            # recv(icmp_socket)
            
            # data_recv_form = icmp_socket.recvfrom(2048)
            # print(data_recv_form)    

            # response, _ = icmp_socket.recvfrom(1024)
            # icmp_type = struct.unpack('!B', response[20:21])[0]
            # print(icmp_type)
            data_recv = icmp_socket.recv(2048)


            data_recv, ip_bool = analyze_ether_header(data_recv)
            # receive_ping(dst_ip)

        # Wait for a short duration before sending packets with next MAC

        time.sleep(0.1)



if __name__ == "__main__":

    main()





# Start the check_packet function in a separate thread

#check_thread = threading.Thread(target=check_packet)

#check_thread.start()



# Wait for the check_

