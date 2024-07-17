import cv2
import numpy as np
import socket
from picamera2 import Picamera2

# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the IP address and port number
ip_address = '192.168.4.82'  # Replace with the IP address of the server
port = 5000

# Bind the socket to the address and port
sock.bind((ip_address, port))

# Listen for incoming connections
sock.listen(1)
print("Waiting for a connection...")

# Accept the connection
conn, addr = sock.accept()
print(f"Connected to {addr}")

# Initialize the Picamera2 object
piCam = Picamera2()
config = piCam.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"})
piCam.configure(config)
piCam.start()

try:
    while True:
        # Capture frame-by-frame
        frame = piCam.capture_array()

        # Encode the frame as JPEG
        encoded, buffer = cv2.imencode('.jpg', frame)

        # Convert the encoded frame to bytes
        frame_data = buffer.tobytes()

        # Get the size of the frame
        size = len(frame_data)

        # Send the size of the frame
        conn.sendall(size.to_bytes(4, byteorder='big'))

        # Send the frame data
        conn.sendall(frame_data)

except KeyboardInterrupt:
    print("Interrupted by user, stopping...")

finally:
    # Release the resources
    piCam.stop()
    cv2.destroyAllWindows()
    conn.close()
    sock.close()
