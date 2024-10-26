from scapy.all import *
import random
import time

def random_ip():
    """Generate a random IP address."""
    return ".".join([str(random.randint(1, 254)) for _ in range(4)])

def random_mac():
    """Generate a random MAC address."""
    return ":".join(["{:02x}".format(random.randint(0, 0xFF)) for _ in range(6)])

def send_arp_request():
    """Send an ARP request with a hidden message."""
    src_ip = random_ip()
    dst_ip = random_ip()
    src_mac = random_mac()
    hidden_message = "ARP is not what you should be filtering for, would you say that 'The-Supermarket' might be some sort of unique header?"

    # Create the ARP request packet with hidden message
    arp = ARP(op=1, pdst=dst_ip, psrc=src_ip)
    ether = Ether(src=src_mac, dst="ff:ff:ff:ff:ff:ff") / arp / Raw(load=hidden_message)
    
    # Send the packet
    sendp(ether, verbose=False)

def send_arp_request_api():
    #send the ARP request every second
    while True:
        send_arp_request()
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        while True:
            send_arp_request()
            time.sleep(0.1) 
    except KeyboardInterrupt:
        print("Script stopped.")
