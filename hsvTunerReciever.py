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

# Create a window
cv2.namedWindow('Frame')

# Create trackbars for HSV
cv2.createTrackbar('H_min', 'Frame', 0, 179, nothing)
cv2.createTrackbar('S_min', 'Frame', 0, 255, nothing)
cv2.createTrackbar('V_min', 'Frame', 0, 255, nothing)
cv2.createTrackbar('H_max', 'Frame', 179, 179, nothing)
cv2.createTrackbar('S_max', 'Frame', 255, 255, nothing)
cv2.createTrackbar('V_max', 'Frame', 255, 255, nothing)

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

    # Get current positions of all trackbars
    h_min = cv2.getTrackbarPos('H_min', 'Frame')
    s_min = cv2.getTrackbarPos('S_min', 'Frame')
    v_min = cv2.getTrackbarPos('V_min', 'Frame')
    h_max = cv2.getTrackbarPos('H_max', 'Frame')
    s_max = cv2.getTrackbarPos('S_max', 'Frame')
    v_max = cv2.getTrackbarPos('V_max', 'Frame')

    # Convert frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define range of HSV values
    lower_hsv = np.array([h_min, s_min, v_min])
    upper_hsv = np.array([h_max, s_max, v_max])

    # Threshold the HSV image
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

    # Bitwise-AND mask and original image
    filtered_frame = cv2.bitwise_and(frame, frame, mask=mask)

    # Display the frame
    cv2.imshow('Frame', filtered_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the resources
cv2.destroyAllWindows()
sock.close()