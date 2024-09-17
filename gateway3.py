import os
import socket
import sqlite3

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
        ciphered_data = conn.recv(1024)
        ciphered_words = [int(word) for word in ciphered_data.decode().split(',')[:-1]]
        nonce = int(ciphered_data.decode().split(',')[-1]).to_bytes(16, byteorder='big')
        print(f"Received ciphered words: {ciphered_words}")
        print(f"Received nonce: {nonce.hex()}")
        # Decrypt the ciphered words using the session key and nonce
        # (Decryption code goes here)