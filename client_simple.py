import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()

# main program
host = '129.82.45.121' # this is the IP address of the blowfish machine (I hope this doesn't change periodically. Idk how to find it other than running the 'hostname -I' command on the host machine)
port = 12358

# Create a client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to the server
client_socket.connect((host, port))

while 1:
    # Get user input
    message = input("Enter a message: ")

    # Send the input to the server
    client_socket.send(message.encode())

    # Receive the server's response
    server_response = client_socket.recv(1024)

    # Print the server's response
    print(f"Server responded with: {server_response.decode()}")

    # Exit condition
    if message == "exit":
        break

# Close the client socket
client_socket.close()