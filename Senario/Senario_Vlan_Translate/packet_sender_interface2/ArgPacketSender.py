import sys
import time
import threading
from scapy.all import Ether, IP, TCP, Dot1Q, sendp, sniff

selectedPort = 50001
dst_ip = '192.168.2.88'
vlan_id = 700
dst_mac = '08:00:27:74:bc:d6'
payload = "Hello, world!"
selectedInterface = "eth0"

def read_mac_addresses(file_path):
    with open(file_path, 'r') as file:
        mac_addresses = [line.strip() for line in file if line.strip()]
    return mac_addresses

def send_packet(src_mac_address, pay_load):
    packet = Ether(src=src_mac_address, dst=dst_mac) / Dot1Q(vlan=vlan_id) / IP(dst=dst_ip) / TCP(dport=selectedPort) / pay_load
    sendp(packet, iface=selectedInterface, verbose=False)

def packet_callback(packet):
    global received
    if packet.haslayer(TCP) and packet[TCP].dport == selectedPort:
        print("Source IP:", packet[IP].src, packet[Ether].src)
        received = True

def check_packet():
    global received
    while True:
        received = False
        sniff_thread = threading.Thread(target=sniff, kwargs={'iface': selectedInterface, 'prn': packet_callback, 'filter': f'tcp port {selectedPort}', 'timeout': 5})
        sniff_thread.start()

        # After sniffing started, send a packet
        send_packet()

        # Wait for the sniffing thread to finish
        sniff_thread.join()

        # Print success or fail
        if received:
            print("Success: Packet received by destination")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_mac.txt>")
        sys.exit(1)

    mac_file_path = sys.argv[1]
    mac_addresses = read_mac_addresses(mac_file_path)

    for mac in mac_addresses:
        send_packet(mac, payload)
        time.sleep(1)  # Optional delay between sending packets

