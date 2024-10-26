"""the purpose of this file is to act as the client in the client server communication for http streams to be captured on wireshark"""

import socket
import time


#global to hold an HTTP request

HTTP_REQUEST = "GET / HTTP/1.1\r\nHost: sendmesomeoreos.com\r\n\r\n"


def main():
    #connect to the server socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 80))

    #send the request
    client_socket.send(HTTP_REQUEST.encode())

    #recieve data from the server
    data = client_socket.recv(1024).decode()

    while data != "DONE": #this is the last message I expect from the server
    
        client_socket.close()

        #simulate time passing before I make a new new request
        time.sleep(0.1)
    
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
        client_socket.connect(("127.0.0.1", 80))

        client_socket.send(HTTP_REQUEST.encode())

        data = client_socket.recv(1024).decode()


    #I finished the loop so close the socket
    client_socket.close()


if __name__ == "__main__":
    main()