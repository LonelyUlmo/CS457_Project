import socket
import selectors
import json
import threading

def receive_messages(sock):
    while True:
        try:
            server_response = sock.recv(4096)
            if server_response:
                response_json = json.loads(server_response.decode())
                message = response_json["message"]
                print("\nServer says:")
                print(f"{message}")
                try:
                    if response_json["liveGame"] == False:
                        client_socket.close()
                        break
                except:
                    pass
            else:
                print("\nConnection closed by the server.")
                break
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

sel = selectors.DefaultSelector()

# main program
host = '129.82.45.121' # this is the IP address of the blowfish machine (I hope this doesn't change periodically. Idk how to find it other than running the 'hostname -I' command on the host machine)
port = 12350

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((host, port))
    print(f"Connected to server at {host}:{port}")

    # Start thread that listens to server
    receiver_thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
    receiver_thread.start()

    # handle user input here; sends the input to server
    while True:
        # Get user input
        user_input = input("")
        print(f"You input: {user_input}")
        message = {"message": user_input}
        # Send input to server
        client_socket.send(json.dumps(message).encode())
        # Exit condition
        if user_input.lower() == "exit":
            print("Disconnecting from the server...")
            break
except Exception as e:
    print(f"Error: conection lost to the server: {e}")
finally:
    client_socket.close()