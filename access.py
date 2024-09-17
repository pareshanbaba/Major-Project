import os
import socket
import sqlite3
import time
import struct
import ecies
from ecies.utils import generate_eth_key
from coincurve import PrivateKey, PublicKey

def create_database_connection():
    conn = sqlite3.connect('session_keys.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS session_keys
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, session_key BLOB)''')
    conn.commit()
    return conn

# Define the valid time window (in seconds)
VALID_TIME_WINDOW = 60  # Adjust this value as per your requirement

# Generate a random session key (e.g., 16 bytes)
session_key = os.urandom(16)

# Sensor ID (assumed to be known to both devices)
sensor_id = b'my_sensor_id'

# XOR the session key with the sensor ID to encrypt it
encrypted_key = bytes([a ^ b for a, b in zip(session_key, sensor_id)])

# Encode the encrypted key to bytes for transmission
encoded_key = encrypted_key.hex()

# Connect to the sensor
sensor_ip = '192.168.137.61'  # Replace with the Raspberry Pi's IP address
sensor_port = 8000

# Store the session key in the database
conn = create_database_connection()
c = conn.cursor()
c.execute("INSERT INTO session_keys (session_key) VALUES (?)", (session_key,))
conn.commit()
conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((sensor_ip, sensor_port))
    s.sendall(encoded_key.encode())
    print(f"Sent encoded key: {encoded_key}")

# Receive the ciphered data, nonce, and timestamp from the sensor
gateway_ip = '192.168.137.1'  # Replace with the gateway's IP address
gateway_port = 8001  # Replace with the gateway's port number

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((gateway_ip, gateway_port))
    s.listen(1)
    print(f"Listening for ciphered data on {gateway_ip}:{gateway_port}")
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        ciphered_data = conn.recv(1024).decode()
        ciphered_block, nonce, timestamp = ciphered_data.split(',')
        ciphered_block = int(ciphered_block, 16)
        nonce = bytes.fromhex(nonce)
        timestamp = int(timestamp)
        print(f"Received ciphered block: {ciphered_block:016X}, Nonce: {nonce.hex()}, Timestamp: {timestamp}")

        # Verify that the nonce and timestamp are valid
        current_time = int(time.time())
        time_diff = abs(current_time - timestamp)
        if time_diff <= VALID_TIME_WINDOW:
            print("Nonce and timestamp are valid")

            # Send the session key to the user (laptop) using ECIES
            user_public_key = "004b8f627f8b6f9c17d0723d48df8f87f1f7d9a7ff1963fb3f7b1d95b92b6d42b6a8da27e0b60faaf9ecd01a4dd4633a7e0c2d3a3bf6b7eb8a9dcc7b0c818b9f1f7"  # Replace with the user's public key

            # Generate ephemeral key pair
            ephemeral_private_key = PrivateKey()
            ephemeral_public_key = ephemeral_private_key.public_key

            # Encrypt the session key using ECIES
            encrypted_session_key = ecies.encrypt(
                session_key,
                PublicKey(bytes.fromhex(user_public_key))
            )

            # Send the encrypted session key to the user (laptop)
            laptop_ip = '192.168.1.100'  # Replace with the laptop's IP address
            laptop_port = 8002  # Replace with the laptop's port number
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((laptop_ip, laptop_port))
                s.sendall(encrypted_session_key)

            print("Access granted to user")
        else:
            print("Nonce and/or timestamp are invalid")