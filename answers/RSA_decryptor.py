"""the purpose of this file is to automate the process of decrypting an RSA encrypted message"""
def is_prime(number):
    """check if a number is prime"""
    for i in range(2, number):
        if number % i == 0:
            return False
    return True

def get_p_and_q(modulus):
    """given a modulus, return its prime factors"""
    for i in range(2, modulus):
        if is_prime(i) and modulus % i == 0: # Check if i is prime and the modulus is divisible by i
            p = i # If the condition is met, i is the first prime factor
            q = modulus // i # The second prime factor is the modulus divided by the first prime factor
            if is_prime(q): # Check if the second prime factor is also prime
                return p, q # If the condition is met, return the two prime factors
    raise ValueError("Could not find prime factors") 

def get_RSA_private_key(p, q, public_key):
    """Calculate the pair of the RSA public key."""
    totient = (p-1)*(q-1)
    for i in range(1, totient): # Loop from 1 to totient to find a number that meets the condition
        if (i*public_key) % totient == 1: #the condition for the private key to be the proper private key
            print("Private key found:", i)
            return i
    raise ValueError("Could not find private key") # If no private key is found, raise an error


def decrypt(message, private_key, modulus):
    """Decrypt the message"""
    decrypted_message = []
    try:
        for num in message.split(): # Loop through each number in the message
            decrypted_value = pow(int(num), private_key, modulus) # Decrypt the number
            decrypted_message.append(chr(decrypted_value)) # Append the decrypted character based on its ascii value to the list
    except ValueError:
        raise RuntimeError("Error: Could not decrypt message")
    return "".join(decrypted_message) # Return the list as a string


def main():

    modulus = eval(input("Enter the modulus: "))

    while not isinstance(modulus, int):
        print("Error: Modulus must be an integer")
        modulus = eval(input("Enter the modulus: "))

    public_key = eval(input("Enter the public key: "))

    while not isinstance(public_key, int):
        print("Error: Public key must be an integer")
        public_key = eval(input("Enter the public key: "))

    encrypted_message = input("Enter the encrypted message: ")

    try:
        p, q = get_p_and_q(modulus)
    except ValueError as error:
        print(error)
        return
    
    try:
        private_key = get_RSA_private_key(p, q, public_key)
    except ValueError as error:
        print(error)
        return

    try:
        decrypted_message = decrypt(encrypted_message, private_key, modulus)
        print("Decrypted message:", decrypted_message)
    except RuntimeError as error:
        print(error)

if __name__ == "__main__":
    main()



