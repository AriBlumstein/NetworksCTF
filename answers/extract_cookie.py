"""The purpose of this file is to extract the information from the cookies with the specified conditions that "The-Supermarket" is present"""

import base64
import sys
from scapy.all import *
from scapy.layers.http import HTTPResponse #this is a must to import, not impicitly imported
def extract_cookie_chunks(pcap_file, output_file):
    """ method responsible for extacting a special chunk from cookies in 
        the http responses that have the header "The-Supermarket" """
    packets = rdpcap(pcap_file)
    with open(output_file, 'wb') as f:
        for pkt in packets:
            if pkt.haslayer(HTTPResponse):  #Check if the packet has as http response
                
                http_layer = pkt[HTTPResponse] 
                
                #now that we have the  http layer, we can check if our unique header, "The-Supermarket", for the packets that have this header field are the packets that have our cookie info

                # "The-Supermarket is the header we are looking for, it is returned as a key in the "Unknown_Headers" dictionary in the scapy produced http layer
                if "Unknown_Headers" in http_layer.fields.keys() and b'The-Supermarket' in http_layer.fields["Unknown_Headers"].keys():

                    #now we can get the cookie chunk from the set cookie header
                    cookie = http_layer.fields['Set_Cookie'].decode(errors='ignore')
                    
                    #find the start of the chunk value, it starts after "chunk="
                    start_index = cookie.find("chunk=") + len("chunk=")

                    #find the end of the chunk value, it ends at the next ";" after the start index
                    end_index = cookie.find(";", start_index)

                    chunk_value = cookie[start_index:end_index] #the full chunk value

                    #now we need to base64 decode the chunk value and write the bytes to the file
                    try:
                        f.write(base64.b64decode(chunk_value))
                    except Exception as err:
                        print("Failed to decode: {} due to {}".format(chunk_value, err))
                        break  

    print("Extraction complete, check {} for the decoded info".format(output_file))        


def main():

    if len(sys.argv) != 2:
        print("Usage: python recreate_executable.py <pcap_file>")
        sys.exit(1)

    if not sys.argv[1].endswith(".pcapng"):
        print("Please provide a pcapng file")
        sys.exit(1)

    #check if file exists
    if not os.path.exists(sys.argv[1]):
        print("File does not exist")
        sys.exit(1)

    pcap_file = sys.argv[1]

    output_file = 'hidden_cookie.txt'

    extract_cookie_chunks(pcap_file, output_file)

if __name__ == "__main__":
    main()