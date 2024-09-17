import socket
import random
import string

# Gateway IP and port
HOST = "192.168.137.1"
PORT = 8000

# Sensor ID to pseudo ID mapping
sensor_mapping = {}

# Generate a random pseudo ID
def generate_pseudo_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(5)

print(f"Gateway listening on {HOST}:{PORT}")

while True:
    # Wait for a connection
    conn, addr = sock.accept()
    print(f"Connected with {addr}")

    try:
        # Receive the sensor ID
        sensor_id = conn.recv(1024).decode()

        # Check if the sensor is already registered
        if sensor_id in sensor_mapping:
            pseudo_id = sensor_mapping[sensor_id]
            message = f"Sensor {sensor_id} already registered with pseudo ID {pseudo_id}"
        else:
            # Generate a new pseudo ID
            pseudo_id = generate_pseudo_id()
            sensor_mapping[sensor_id] = pseudo_id
            message = f"User registered with gateway"

        print(message)

        # Send a response back to the sensor
        conn.sendall(message.encode())

    finally:
        # Clean up the connection
        conn.close()