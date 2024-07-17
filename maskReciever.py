import cv2
import numpy as np
import socket

def nothing(x):
    pass

# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the IP address and port number
ip_address = '192.168.4.82'
port = 5000

# Connect to the server
sock.connect((ip_address, port))

# Create a loop to continuously receive and display frames
while True:
    # Function to receive a single mask
    def receive_mask():
        # Receive the size of the mask
        size = sock.recv(4)
        size = int.from_bytes(size, byteorder='big')

        # Receive the mask data
        data = b''
        while len(data) < size:
            packet = sock.recv(size - len(data))
            if not packet:
                break
            data += packet

        # Convert the received data to a numpy array
        mask_data = np.frombuffer(data, dtype=np.uint8)

        # Decode the mask
        mask = cv2.imdecode(mask_data, cv2.IMREAD_GRAYSCALE)
        return mask

    # Receive the blue mask
    blue_mask = receive_mask()

    # Receive the yellow mask
    yellow_mask = receive_mask()

    # Combine masks into one image for display (optional)
    combined_mask = cv2.bitwise_or(blue_mask, yellow_mask)

    # Display the blue mask
    cv2.imshow('Blue Mask', blue_mask)
    
    # Display the yellow mask
    cv2.imshow('Yellow Mask', yellow_mask)

    # Display the combined mask
    cv2.imshow('Combined Mask', combined_mask)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the resources
cv2.destroyAllWindows()
sock.close()
