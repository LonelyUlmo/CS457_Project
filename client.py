import socket
import selectors
import json

sel = selectors.DefaultSelector()

# main program
host = '129.82.45.121' # this is the IP address of the blowfish machine (I hope this doesn't change periodically. Idk how to find it other than running the 'hostname -I' command on the host machine)
port = 12358

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

server_response = client_socket.recv(4096)
print(f"Server says: {server_response.decode()}")

while 1:
    # message = input("Enter a message: ")
    action = input("Enter an action: ")
    message = {
        "action": action
    }

    # Send the input to the server
    client_socket.send(json.dumps(message).encode())

    # Receive the server's response
    server_response = client_socket.recv(4096)
    print(f"Server responded with: {server_response.decode()}")

    # Exit condition
    if action == "exit":
        break

client_socket.close()