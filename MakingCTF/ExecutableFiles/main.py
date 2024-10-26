import sys
from certificate_creator import certificate_sender
from http_server import http_server_ctf

def main():
    """driver code for entire executable"""
    try:
        certificate_sender()
        print("Opening the HTTP server that you were told about...")
        http_server_ctf()
    except Exception as e:
        print(e)
        sys.exit()

if __name__ == "__main__":
    main()
   


