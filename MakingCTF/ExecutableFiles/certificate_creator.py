"""the purpose of this file is to make a mock self signed certificate for the client to send to the server"""

from cryptography import x509 #certificate
from cryptography.x509.oid import NameOID, ObjectIdentifier #for the general parts of a certificate, ObjectID for the extensions
from cryptography.hazmat.primitives import hashes #hashing algorithm
from cryptography.hazmat.primitives.asymmetric import rsa #signing of the certificate
from cryptography.hazmat.primitives import serialization #serializing the certificate to pem format 
from datetime import datetime, timedelta, timezone #date and time for the certificate
import socket # to send the certificate
import protocols # general use protocols for the ctf

MESSAGE = "If you really want to find Ariel visit {}, I have provided you with 'credentials' to properly 'query' with".format(protocols.SERVER)

def certificate_builder():
    """the purpose of this function is to create a mock certificate for the client to send to the server"""
    
    # Generate private key for signing the certificate
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    # Generate a public key
    public_key = private_key.public_key()

    # Create a builder for the certificate
    builder = x509.CertificateBuilder() #framework for public key certificates

    # Set certificate details, general details within a certificate
    builder = builder.subject_name(x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "il"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Jerusalem"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Jerusalem"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Find the Missing student"),
        x509.NameAttribute(NameOID.COMMON_NAME, protocols.SERVER)
    ]))


    #add the issuer to the certificate, it's general details
    builder = builder.issuer_name(x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "il"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Jerusalem"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Jerusalem"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "CTF certificate issuer"),
        x509.NameAttribute(NameOID.COMMON_NAME, "ctf.com")
    ]))

    #add the validity dates to the certificate
    now = datetime.now(timezone.utc)
    builder = builder.not_valid_before(now)
    builder = builder.not_valid_after(now + timedelta(days=30))

    #unique serial number
    builder = builder.serial_number(x509.random_serial_number())
    
    #assign the public key
    builder = builder.public_key(public_key)


    #we will now add out fake extensions to the certificate for the purpose of the ctf
    builder = builder.add_extension(
        x509.UnrecognizedExtension(ObjectIdentifier("1.2.3.4.5.6.7.8.1"), MESSAGE.encode()),
        critical=True
    )

    builder = builder.add_extension(
        x509.UnrecognizedExtension(ObjectIdentifier("1.2.3.4.5.6.7.8.2"), protocols.CERTIFICATE_USERNAME.encode()),
        critical=True
    )

    builder = builder.add_extension(
        x509.UnrecognizedExtension(ObjectIdentifier("1.2.3.4.5.6.7.8.3"), protocols.CERTIFICATE_PASSWORD.encode()),
        critical=True
    )

    # Sign the certificate with the private key
    certificate = builder.sign(private_key=private_key, algorithm=hashes.SHA256())

    # Convert the certificate to PEM format
    certificate_pem = certificate.public_bytes(serialization.Encoding.PEM)

    return certificate_pem

def certificate_sender():

    # Client setup
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    try:
        client_socket.connect((protocols.SERVER, protocols.CERTIFICATE_PORT))
    except Exception: #if the server is not running
        raise Exception("I have a file I'm trying to send to the host '{}' on port {} but it doesn't seem to be running...".format(protocols.SERVER, protocols.CERTIFICATE_PORT))

    # Build the certificate
    certificate_pem = certificate_builder()
    
    # Send the certificate

    # send the size of the file that needs to be sent to the server
    client_socket.send(("The size of the certificate is " + str(len(certificate_pem))).encode())

    response = client_socket.recv(1024).decode() #wait for the server to acknowledge the size

    #check the server followed the proper protocol
    PROPER_RESPONSE = protocols.SIZE_OK.format(str(len(certificate_pem)))

    if response != PROPER_RESPONSE:
        raise Exception("Expected {}, but received '{}'. Please check the server status or protocol implementation.".format(PROPER_RESPONSE, response))
    
    #ask for permission to begin transmitting
    client_socket.send(protocols.REQUEST_PERMISSION.encode())

    response = client_socket.recv(1024).decode() #wait for the server to acknowledge the size

    #check the server followed the proper protocol
    if response != protocols.PERMISSION_TO_SEND:
        raise Exception("Expected {}, but received '{}'. Please check the server status or protocol implementation.".format(protocols.PERMISSION_TO_SEND, response))

    client_socket.send(certificate_pem)

    # Close the connection
    client_socket.close()

if __name__ == "__main__":
    try:
        certificate_sender()
    except Exception as e:
        print(e)


