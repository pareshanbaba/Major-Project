import os
import socket

# Generate a random session key (e.g., 16 bytes)
session_key = os.urandom(16)

# Sensor ID (assumed to be known to both devices)
sensor_id = b'my_sensor_id'

# XOR the session key with the sensor ID to encrypt it
encrypted_key = bytes([a ^ b for a, b in zip(session_key, sensor_id)])
#print("Encrypted_Key",encrypted_key)
# Encode the encrypted key to bytes for transmission
encoded_key = encrypted_key.hex()
#print("Encoded",encoded_key)

# Connect to the sensor
sensor_ip = '192.168.137.165'  # Replace with the Raspberry Pi's IP address
sensor_port = 8000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((sensor_ip, sensor_port))
    s.sendall(encoded_key.encode())