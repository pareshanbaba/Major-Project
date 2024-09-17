from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import socket

# Encryption Process

# Generate the sender's ephemeral keys 
sender_private_key = ec.generate_private_key(ec.SECP256K1())
sender_public_key = sender_private_key.public_key()

# Generate receiver's public and private key (Do this once and provide the public key to the sender)
receiver_private_key = ec.generate_private_key(ec.SECP256K1())
receiver_public_key = receiver_private_key.public_key()

# Compute the shared secret
shared_key = sender_private_key.exchange(ec.ECDH(), receiver_public_key)

# Derive the encryption key using HKDF
derived_key = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b'encryption key'
).derive(shared_key)

# Encrypt the data
plaintext = b"My secret message" 
cipher = Cipher(algorithms.AES(derived_key), modes.GCM(derived_key[:12]))
encryptor = cipher.encryptor()
ciphertext = encryptor.update(plaintext) + encryptor.finalize()
tag = encryptor.tag
print("Tag Length (Sender):", len(tag))

# Send data to the receiver
HOST = '192.168.1.2'  # Replace with the Raspberry Pi's IP address
PORT = 5000 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect((HOST, PORT))

try:
    # Send the sender's ephemeral public key
    s.sendall(sender_public_key.public_bytes(
        encoding=serialization.Encoding.PEM, 
        format=serialization.PublicFormat.SubjectPublicKeyInfo)
    )

    # Send the ciphertext
    s.sendall(ciphertext)

    # Send the authentication tag
    s.sendall(tag)

finally:
    s.close()
