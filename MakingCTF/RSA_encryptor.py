
"""This file encrypts the final message of the ctf, one char at a time, using the RSA algorithm"""
def RSA_encrypt(message, public_key, modulus):
    encrypted_message = [] 
    for char in message:
        ascii_value = ord(char) #get the ascii value of the character
        encrypted_value = pow(ascii_value, public_key, modulus) #encrypt the ascii value
        encrypted_message.append(encrypted_value) #add the encrypted value to the list
    return " ".join(str(x) for x in encrypted_message) #return the list as a string, this is our full encrypted message

def main():
    #set up the values for encryption, including the message, the public key, and the modulus
    message = "Ariel didn't disappear, he graduated! He extends his heartfelt gratitude to his many teachers for all their guidance and hopes to make them proud as he embarks on his professional journey! Thank you for participating in this CTF, one of his final projects in school."
    public_key = 17
    modulus = 3233
    encrypted_message = RSA_encrypt(message, public_key, modulus)
    print("Encrypted message:", encrypted_message)

if __name__ == "__main__":
    main()


