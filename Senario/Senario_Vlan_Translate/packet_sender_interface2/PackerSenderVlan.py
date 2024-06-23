from scapy.all import Ether, IP, TCP, sendp, sniff, Raw, Dot1Q
import threading 

import time


selectedPort=50001

dst_ip='192.168.120.5'

vlan_id=700

dst_mac='d0:37:45:a7:1e:a9'


#packet = Ether(src='00:11:22:33:44:55', dst='08:00:27:74:bc:d6') / IP(dst=dst_ip) / #TCP(dport=selectedPort)

    # Adding Dot1Q layer with VLAN ID 700

#packet = Ether(src=src_mac, dst=dst_mac) / \

#     Dot1Q(vlan=vlan_id) / \

#     IP(dst=dst_ip) / \

#     TCP(dport=selectedPort) / \

#     payload



selectedInterface="eth0"





def read_mac_addresses(file_path):

    with open(file_path, 'r') as file:

        mac_addresses = [line.strip() for line in file if line.strip()]

    return mac_addresses



def send_packet(src_mac_address,pay_load):

    # Craft an Ethernet frame with the desired source and destination MAC addresses
    custom_payload = b'\xaa' * 466
    ip_pkt = IP(dst=dst_ip, ttl=255, proto=254)
    ether_pkt = Ether(dst=dst_mac, src=src_mac_address)
    packet = ether_pkt / ip_pkt / Raw(load=custom_payload)
    print(src_mac_address) 

    # Send the packet

    sendp(packet, iface=selectedInterface, verbose=False)



def packet_callback(packet):

    global received

    if packet.haslayer(TCP) and packet[TCP].dport == 50001 :

        print("Source IP:", packet['IP'].src, packet['Ether'].src)

        received = True



def check_packet():

    global received

    while True:

        received = False

        sniff_thread = threading.Thread(target=sniff, kwargs={'iface': selectedInterface, 'prn': packet_callback, 'filter': 'tcp port 50001', 'timeout': 5})

        sniff_thread.start()

        

        # After sniffing started, send a packet

        send_packet()



        # Wait for the sniffing thread to finish

        sniff_thread.join()



        # Print success or fail

        if received:

            print("Success: Packet received by destination")

        else:

            print("Fail: Remote PC did not receive the packet within the timeout")



        # Sleep for a while before sending the next packet

        time.sleep(0.3)  # Adjust this value as needed





def main():

    mac_addresses = read_mac_addresses('/home/mac.txt')

    num_macs = len(mac_addresses)

    while True:

        for src_mac in mac_addresses:

            payload = "Hello, world!"

            send_packet(src_mac, payload)

            time.sleep(0.1)

        # Wait for a short duration before sending packets with next MAC

        time.sleep(0.1)



if __name__ == "__main__":

    main()





# Start the check_packet function in a separate thread

#check_thread = threading.Thread(target=check_packet)

#check_thread.start()



# Wait for the check_

