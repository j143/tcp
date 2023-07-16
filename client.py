import socket

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = ('localhost', 8080)
client_socket.connect(server_address)

# Send data to the server
message = "Hello, server!"
print(f"Sending message: {message}")
client_socket.sendall(message.encode())

# Receive data from the server
data = client_socket.recv(1024)
print(f"Received message: {data.decode()}")


# Receive the file data from the server
file_data = client_socket.recv(1024)

# Decode the file data into a string
file_contents = file_data.decode()

# Print the file contents to the screen
print(file_contents)

# Save the file data to a file
with open('received.txt', 'wb') as f:
    f.write(file_data)

# Close the socket
client_socket.close()
