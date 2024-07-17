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

# Define HSV range for blue color
blue_lower = np.array([85, 19, 97])
blue_upper = np.array([175, 255, 255])

# Define HSV range for yellow color
yellow_lower = np.array([4, 104, 57])
yellow_upper = np.array([55, 255, 255])

try:
    while True:
        # Capture frame-by-frame
        frame = piCam.capture_array()

        # Convert the frame to HSV color space
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

        # Create a mask for the blue color
        blue_mask = cv2.inRange(hsv_frame, blue_lower, blue_upper)

        # Create a mask for the yellow color
        yellow_mask = cv2.inRange(hsv_frame, yellow_lower, yellow_upper)

        # Encode the blue mask as JPEG
        encoded_blue, buffer_blue = cv2.imencode('.jpg', blue_mask)

        # Convert the encoded blue mask to bytes
        blue_data = buffer_blue.tobytes()

        # Get the size of the blue mask
        size_blue = len(blue_data)

        # Send the size of the blue mask
        conn.sendall(size_blue.to_bytes(4, byteorder='big'))

        # Send the blue mask data
        conn.sendall(blue_data)

        # Encode the yellow mask as JPEG
        encoded_yellow, buffer_yellow = cv2.imencode('.jpg', yellow_mask)

        # Convert the encoded yellow mask to bytes
        yellow_data = buffer_yellow.tobytes()

        # Get the size of the yellow mask
        size_yellow = len(yellow_data)

        # Send the size of the yellow mask
        conn.sendall(size_yellow.to_bytes(4, byteorder='big'))

        # Send the yellow mask data
        conn.sendall(yellow_data)

except KeyboardInterrupt:
    print("Interrupted by user, stopping...")

finally:
    # Release the resources
    piCam.stop()
    cv2.destroyAllWindows()
    conn.close()
    sock.close()
