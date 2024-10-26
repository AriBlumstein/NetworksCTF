"""the purpose of this file is to act as the server in the client server communication for http streams to be captured on wireshark"""
import socket
import base64
import sys 
from tqdm import tqdm

# Define server address and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 80 

# Read and encode the file
if len(sys.argv) != 2:
    print("Usage: python create_cookie_server.py <filename>")
    exit()

try:
    with open(sys.argv[1], 'rb') as file:
        executable_data = file.read()
except FileNotFoundError:
    print("File not found")
    exit()

# Define chunk size
chunk_size = 2000

# Split the data into chunks and encode each chunk with Base64
encoded_chunks = [base64.b64encode(executable_data[i:i + chunk_size]).decode('utf-8')
                  for i in range(0, len(executable_data), chunk_size)]


# Function to generate headers for each chunk as HTTP response with cookies
def generate_resposne(chunk_index, unique_id, message="a 'chunk' of something bigger is hidden here..."):
    """ we will be sending a http response with the current index value of the broken up executable """
    
    headers = "HTTP/1.1 200 OK\r\n"
    headers += "Content-Type: text/html\r\n"
    headers += "Content-Length: {}\r\n".format(len(message))
    headers += "The-Supermarket: {}\r\n".format(unique_id)
    headers += "Set-Cookie: sessionID=ctf; path=/; Domain=sendmesomeoreos.com; chunk={};\r\n".format(encoded_chunks[chunk_index])
    headers += "Connection: close\r\n"
    headers += "\r\n"

    #add the easter egg to say something is hidden
    headers += message
    return headers

def handle_client(client_socket, chunk_index):
    """function responsible for recieveing the request from the mock client"""

    unique_id = "shufersal"
    try:
        if chunk_index < len(encoded_chunks):
            headers = generate_resposne(chunk_index, unique_id)
            response_data = headers.encode()
            client_socket.send(response_data)
        else:
            client_socket.send("DONE".encode())
    
    except Exception as e:
        print("Error sending data: {}".format(e))
        sys.exit()
    
    finally:
       client_socket.close()


def main():
    """driver code to make a mock http streams"""

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the server address and port
    server_socket.bind((SERVER_HOST, SERVER_PORT))

    # Listen for incoming connections 
    server_socket.listen(1)
    print("[*] Listening on {}:{}".format(SERVER_HOST, SERVER_PORT))

    print("packets to send: ", len(encoded_chunks)+1)

    # Main server loop
    for x in tqdm(range(len(encoded_chunks)+1)):

        # Wait for a connection
        client_socket, client_address = server_socket.accept()

        #recieve request from client socket 
        request = client_socket.recv(1024).decode()

        #send the next chunk or DONE
        handle_client(client_socket, x)

if __name__ == "__main__":
    main()