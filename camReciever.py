import cv2
import numpy as np
import socket

# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the IP address and port number
ip_address = '192.168.4.82'
port = 5000

# Connect to the server
sock.connect((ip_address, port))

# Create a loop to continuously receive and display frames
while True:
    # Receive the size of the frame
    size = sock.recv(4)
    size = int.from_bytes(size, byteorder='big')

    # Receive the frame data
    data = b''
    while len(data) < size:
        packet = sock.recv(size - len(data))
        if not packet:
            break
        data += packet

    # Convert the received data to a numpy array
    frame_data = np.frombuffer(data, dtype=np.uint8)

    # Decode the frame
    frame = cv2.imdecode(frame_data, cv2.IMREAD_COLOR)

    # Display the frame
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the resources
cv2.destroyAllWindows()
sock.close()