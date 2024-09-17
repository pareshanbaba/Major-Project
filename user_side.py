import socket
import random
import string

# Gateway IP and port
HOST = "192.168.137.1"
PORT = 8000

# User ID to pseudo ID mapping
user_mapping = {}

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
        # Receive the client type (user)
        client_type = conn.recv(1024).decode()

        if client_type == "user":
            # User registration
            user_id = conn.recv(1024).decode()
            password = conn.recv(1024).decode()

            # Check if the user is already registered
            if user_id in user_mapping:
                pseudo_id = user_mapping[user_id]
                message = f"User {user_id} already registered with pseudo ID {pseudo_id}"
            else:
                # Generate a new pseudo ID
                pseudo_id = generate_pseudo_id()
                user_mapping[user_id] = pseudo_id
                message = f"User {user_id} registered with pseudo ID {pseudo_id}"

            print(message)
            conn.sendall(message.encode())

    finally:
        # Clean up the connection
        conn.close()