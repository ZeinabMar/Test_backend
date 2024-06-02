from scapy.all import sniff

from datetime import datetime



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

    sniff(prn=packet_callback, filter='tcp port 50001', store=False)



if __name__ == "__main__":

    main()

