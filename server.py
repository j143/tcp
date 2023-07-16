import signal
import socket
import sys
import platform
import ifaddr
import subprocess
from scapy.all import *

def signal_handler(sig, frame):
    print('Shutting down server...')
    # Close the server socket
    server_socket.close()
    # Exit the program
    sys.exit(0)

# Register the signal handler for SIGINT
signal.signal(signal.SIGINT, signal_handler)

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('localhost', 8080)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)
print(f"Server listening on {server_address[0]}:{server_address[1]}")

# Get the list of network interfaces based on the platform
# if platform.system() == 'Linux':
#     # Linux command to get the list of interfaces
#     interfaces_command = 'ip link show | awk \'{print $2}\' | sed \'s/://\''
# else:
# Windows command to get the list of interfaces
interfaces_command = 'wmic nic get NetConnectionID'

# Execute the command to get the interfaces
interfaces_process = subprocess.Popen(interfaces_command, shell=True, stdout=subprocess.PIPE)
interfaces_output = interfaces_process.stdout.read().decode().splitlines()

# Filter out loopback interfaces if needed
interfaces = [
    interface_name
    for interface_name in interfaces_output
    if 'loopback' not in interface_name.lower()
]

while True:

    # Check for the SIGINT signal
    signal.signal(signal.SIGINT, signal_handler)
    
    # Wait for a connection
    print("Waiting for a connection...")
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address[0]}:{client_address[1]}")

    # Start capturing packets
    packets = sniff(filter="tcp", iface=['Ethernet','vEthernet (Default Switch)'], count=10)

    # Print the captured packets
    for packet in packets:
        if TCP in packet:
            print(f"Sequence Number: {packet[TCP].seq}")
            if packet[TCP].flags.S:
                print("SYN packet")
            if packet[TCP].flags.A:
                print("ACK packet")

    # Receive data from the client
    data = client_socket.recv(1024)
    print(f"Received message: {data.decode()}")

    ## You can EDIT the response to send a custom message to client
    # Send a response back to the client
    response = "Hello, this is 2023 year"
    client_socket.sendall(response.encode())

    # Open the file to be sent
    with open('example.txt', 'rb') as f:
        # Read the contents of the file
        file_data = f.read()

        # Send the file data to the client
        client_socket.sendall(file_data)

    # Close the client socket
    client_socket.close()
