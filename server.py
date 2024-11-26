import sys
import socket
import selectors
import types
import logging
import json

import TicTacToe

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
# Set up the Logger Here.
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(message)s',
    handlers=[
        logging.FileHandler("serverLogs.log", mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger()

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
# Server logic here
sel = selectors.DefaultSelector()

client_count = 0

def accept_wrapper(sock):
    # Accept the connection
    conn, addr = sock.accept()
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, outb=b"")
    sel.register(conn, selectors.EVENT_READ | selectors.EVENT_WRITE, data=data)
    # logger.info(f"[accept_wrapper] Accepted connection from {addr}.")
    logger.info(f"Accepted connection from {addr}")
    # Save connection to clients
    clientID = get_new_client_ID()
    clients[conn] = clientID
    logger.info(f"[accept_wrapper] Saved {addr} to list of Clients.")
    team = accept_player(conn)
    # Send welcome message
    welcome_message = {
        "message": "Connection Accepted.",
        "clientID": clientID,
        "team": team
        }
    conn.send(json.dumps(welcome_message).encode())
    logger.info(f"[accept_wrapper] Sent welcome message to {addr}.")
    # Try to start a game
    if check_game_ready():
        # send board to players
        message = {
            "message": "Let the game begin!",
            "turn": game.turn,
            "board": game.getPrintableBoard()
        }
        X_player.send(json.dumps(message).encode())
        O_player.send(json.dumps(message).encode())
        logger.info(f"[accept_wrapper] Game Start message sent to players.")

def get_new_client_ID():
    global client_count
    new_ID = client_count
    client_count += 1
    return new_ID

def accept_player(conn):
    global X_player, O_player
    if X_player == None:
        X_player = conn
        return "X"
    elif O_player == None:
        O_player = conn
        return "O"
    return "No team"

def check_game_ready():
    return X_player != None and O_player != None

def remove_player(sock):
    global X_player, O_player
    if X_player == sock:
        X_player = None
    elif O_player == sock:
        O_player = None

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(4096)  # Receive data
        if recv_data:
            logger.info(f"[service_connection] Received \"{recv_data.decode()}\" from {data.addr}")
            data.outb += recv_data  # Prepare to echo data back
        else:
            close_client_connection(sock, data)
    if mask & selectors.EVENT_WRITE and data.outb:
        handle_client_message(sock, data)

def handle_client_message(sock, data):
    logger.info(f"[handle_client_message] Echoing {repr(data.outb)} to {data.addr}")
    sent = sock.send(data.outb)  # Echo data
    data.outb = data.outb[sent:]  # Keep the part of message that hasn't been sent

def close_client_connection(sock, data):
    logger.info(f"[close_client_connection] Closing connection to {data.addr}, client: {clients[sock]}")
    sel.unregister(sock)
    sock.close()
    del clients[sock]
    remove_player(sock)

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
# Main program setup
host = '0.0.0.0'  # Listen on all network interfaces
port = 12359

# Set up the listening socket and register it with the selector
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen() # Could alter this to accept a set number of connections
logger.info(f"Listening on {(host, port)}")
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

# Keep track of clients
clients = {}
X_player = None
O_player = None

# Initialize the Game
game = TicTacToe.TicTacToe(TicTacToe.Role.SERVER, logger)

# Main event loop
try:
    while True:
        for key, mask in sel.select(timeout=None):
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    logger.critical("Caught keyboard interrupt, exiting")
finally:
    sel.close()
    logging.shutdown()
