from scapy.all import *
import random
import time

def random_ip():
    """Generate a random IP address."""
    return ".".join([str(random.randint(1, 254)) for _ in range(4)])

def send_icmp_ping():
    """Send an ICMP Echo Request (ping) with a custom message to a random IP address."""
    target_ip = random_ip()
    message = "ICMP is not what you should be filtering for, what type of snack is an oreo?"
    
    # Create the ICMP Echo Request packet with the custom message as payload
    icmp_ping = IP(dst=target_ip) / ICMP(type=8) / Raw(load=message)

    # Send the packet and receive the response
    response = sr1(icmp_ping, timeout=0.5, verbose=False)

def send_icmp_ping_api():
    """Send an ICMP Echo Request (ping) with a custom message to a random IP address, every second."""
    while True:
        send_icmp_ping()
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        while True:
            send_icmp_ping()
            time.sleep(0.1) 
    except KeyboardInterrupt:
        print("Script stopped.")
