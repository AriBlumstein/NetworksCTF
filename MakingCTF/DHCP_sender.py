from scapy.all import *
import random
import time

def random_mac():
    """Generate a random MAC address."""
    return ":".join(["{:02x}".format(random.randint(0x00, 0xFF)) for _ in range(6)])

def send_dhcp_request():
    """Send a DHCP request with a random MAC address and a hidden message."""
    mac = random_mac()

    # Create the Ethernet frame
    ether = Ether(src=mac, dst="ff:ff:ff:ff:ff:ff")

    # Create the IP packet
    ip = IP(src="0.0.0.0", dst="255.255.255.255")

    # Create the UDP packet
    udp = UDP(sport=68, dport=67)

    # Create the BOOTP packet
    bootp = BOOTP(chaddr=[mac2str(mac)], xid=random.randint(0, 0xFFFFFFFF), flags=0x8000)

    # Hidden message in the DHCP vendor class ID option
    hidden_message = "DHCP is not what you should be filtering for, what protocol does a browser use to communicate with the server?"

    # Create the DHCP packet with the hidden message in the vendor class ID option
    dhcp = DHCP(options=[("message-type", "discover"), 
                         ("vendor_class_id", hidden_message),
                         "end"])

    # Stack the layers to form the complete packet
    dhcp_request = ether / ip / udp / bootp / dhcp

    # Send the packet
    sendp(dhcp_request, verbose=False)

def send_dhcp_request_api():
    """Send a DHCP request with a random MAC address and a hidden message, every second."""
    while True:
        send_dhcp_request()
        time.sleep(0.1)
    

if __name__ == "__main__":
    "testing purposes"
    try:
        while True:
            send_dhcp_request()
            time.sleep(0.1)  
    except KeyboardInterrupt:
        print("Script stopped.")
