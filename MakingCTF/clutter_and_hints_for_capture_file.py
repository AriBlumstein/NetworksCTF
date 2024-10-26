import threading
import signal
import sys
import time
from ARP_request import send_arp_request_api
from ICMP_ping import send_icmp_ping_api
from DHCP_sender import send_dhcp_request_api

# Global flag to signal stopping
stop_event = threading.Event()

def run_thread(target):
    """Run a function in a thread."""
    def wrapper():
        target() #call the function in the threead
        # Check for stop event at intervals
        while not stop_event.is_set():
            time.sleep(0.1)
    thread = threading.Thread(target=wrapper)
    thread.daemon = True  # Daemonize thread (run in background)
    thread.start()
    return thread

def signal_handler(sig, frame):
    """Handle keyboard interrupt (Ctrl+C)."""
    print("\nStopping threads...")
    stop_event.set()  # Signal threads to stop
    sys.exit(0)

def main():
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)

    # Create and start threads for each function
    threads = [
        run_thread(send_arp_request_api),
        run_thread(send_icmp_ping_api),
        run_thread(send_dhcp_request_api)
    ]

    # Wait for threads to finish (they won't, because they run infinite loops)
    try:
        while any(thread.is_alive() for thread in threads):
            time.sleep(1)  # Wait for threads to complete
    except KeyboardInterrupt:
        pass #shutdown script

if __name__ == "__main__":
    main()
