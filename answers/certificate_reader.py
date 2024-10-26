import socket
TIME_OUT = 0.5

def receive_certificate(server_address, port, output_file_path):
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the address and port
    server_socket.bind((server_address, port))

    # Listen for incoming connections
    server_socket.listen()

    # Accept a connection
    client_socket, client_address = server_socket.accept()

    #set timeout for the socket
    client_socket.settimeout(TIME_OUT)

    #recieved the file size
    data = client_socket.recv(1024).decode()

    # get the size of the file the client wants to send
    file_size = eval(data.split(" ")[-1])

    #follow the "protocol"
    client_socket.send("OK: {}".format(file_size).encode())

    #recieve the requet permission
    data = client_socket.recv(1024).decode()

    # follow the "protocol" and grant permission
    client_socket.send("BEGIN TRANSMISSION".encode())

    #recieve the file
    data = client_socket.recv(file_size)

    print(data)

    #save the file
    with open(output_file_path, "wb") as f:
        f.write(data)

    #close the socket
    client_socket.close()
    server_socket.close()


# Run the server
if __name__ == "__main__":
    try:
        receive_certificate("127.0.0.1", 3000, "received_certificate.crt")
    except socket.timeout:
        print("Connection timed out, file may not be complete")
