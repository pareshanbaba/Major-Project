import socket
import uuid
import sqlite3

# Create a database connection
conn = sqlite3.connect('sensor_ids.db')
c = conn.cursor()

# Create a table to store sensor ID mappings
c.execute('''CREATE TABLE IF NOT EXISTS sensor_mappings
             (sensor_id TEXT, temp_id TEXT)''')

# Set up the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('192.168.137.61', 8000))
s.listen(5)

while True:
    conn, addr = s.accept()
    print(f"Connection from {addr}")

    # Receive sensor ID from the Raspberry Pi
    sensor_id = conn.recv(1024).decode()

    # Generate a temporary ID
    temp_id = str(uuid.uuid4())

    # Store the mapping in the database
    c.execute("INSERT INTO sensor_mappings (sensor_id, temp_id) VALUES (?, ?)", (sensor_id, temp_id))
    conn.commit()

    # Send the temporary ID back to the Raspberry Pi
    conn.sendall(temp_id.encode())

    conn.close()

conn.close()