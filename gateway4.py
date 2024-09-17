import os
import socket
import sqlite3
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_public_key, Encoding, PublicFormat

def create_database_connection():
    conn = sqlite3.connect('session_keys.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS session_keys (id INTEGER PRIMARY KEY AUTOINCREMENT, session_key BLOB)''')
    conn.commit()
    return conn

# Generate a random session key (e.g., 16 bytes)
session_key = os.urandom(16)

# Sensor ID (assumed to be known to both devices)
sensor_id = b'my_sensor_id'

# XOR the session key with the sensor ID to encrypt it
encrypted_key = bytes([a ^ b for a, b in zip(session_key, sensor_id)])

# Encode the encrypted key to bytes for transmission
encoded_key = encrypted_key.hex()

# Connect to the sensor
sensor_ip = '192.168.137.165'  # Replace with the Raspberry Pi's IP address
sensor_port = 8000
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((sensor_ip, sensor_port))
    s.sendall(encoded_key.encode())
    print(f"Sent encoded key: {encoded_key}")

# Store the session key in the database
conn = create_database_connection()
c = conn.cursor()
c.execute("INSERT INTO session_keys (session_key) VALUES (?)", (session_key,))
conn.commit()
conn.close()

# Receive the ciphered data and nonce from the sensor
gateway_ip = '192.168.137.1'  # Replace with the gateway's IP address
gateway_port = 8001  # Replace with the gateway's port number
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((gateway_ip, gateway_port))
    s.listen(1)
    print(f"Listening for ciphered data on {gateway_ip}:{gateway_port}")
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        ciphered_words_bytes = conn.recv(1024)
        ciphered_words = [int.from_bytes(ciphered_words_bytes[i:i+2], byteorder='big') for i in range(0, len(ciphered_words_bytes), 2)]
        nonce = conn.recv(16)
        print(f"Received ciphered words: {ciphered_words}")
        print(f"Received nonce: {nonce.hex()}")

        # Receive the public key from the user side (laptop)
        laptop_ip = '192.168.137.95'  # Replace with the laptop's IP address
        laptop_port = 8002  # Replace with the laptop's port number

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((laptop_ip, laptop_port))
            s.listen(1)
            print(f"Waiting for public key from {laptop_ip}:{laptop_port}")
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                received_public_key = conn.recv(1024)

        # Load the received public key
        public_key = load_pem_public_key(received_public_key, default_backend())

        # Encrypt the session key using ECIES
        ephemeral_private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
        ciphertext, ephemeral_public_key_bytes = public_key.encrypt(
            session_key,
            ephemeral_private_key.public_key().public_bytes(
                encoding=Encoding.X962,
                format=PublicFormat.UncompressedPoint
            )
        )

        # Send the encrypted session key and ephemeral public key to the user side (laptop)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((laptop_ip, laptop_port))
            s.sendall(ciphertext)
            s.sendall(ephemeral_public_key_bytes)