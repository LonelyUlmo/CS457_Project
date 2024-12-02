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
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    sel.register(conn, selectors.EVENT_READ | selectors.EVENT_WRITE, data=data)
    logger.info(f"Accepted connection from {addr}")
    # Save connection to clients
    clientID = get_new_client_ID()
    clients[conn] = clientID
    logger.info(f"[accept_wrapper] Saved {addr} to list of Clients.")
    # If two players are already connected, drop this third connection
    if X_player != None and O_player != None:
        close_client_connection(conn, data)
        return
    player_team = accept_player(conn)
    # Send welcome message
    welcome_message = {
        "message": f"Connection Accepted."
        }
    conn.send(json.dumps(welcome_message).encode())
    logger.info(f"[accept_wrapper] Sent welcome message to {addr}.")
    # Try to start a game
    if check_game_ready():
        # Initialize the Game
        game = TicTacToe.TicTacToe(TicTacToe.Role.SERVER, logger)
        game.liveGame = True
        # send starting board to players
        message_content = "Let the game begin!\n"
        message_content += game.getPrintableBoard()
        message_content += (f"It's player {game.turn}'s turn.")
        X_message = { "message": f"{message_content}\nYou are team X" }
        O_message = { "message": f"{message_content}\nYou are team O" }
        X_player.send(json.dumps(X_message).encode())
        O_player.send(json.dumps(O_message).encode())
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
    # Recieve the client message.
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(4096)  # Receive data
        if recv_data:
            logger.info(f"[service_connection] Received \"{recv_data.decode()}\" from {data.addr}")
            data.inb += recv_data  # Prepare to echo data back
        else:
            close_client_connection(sock, data)
    # Msesage has been read.
    if mask & selectors.EVENT_WRITE and data.inb:
        handle_client_message(sock, data)

def handle_client_message(sock, data):
    if sock != X_player and sock != O_player:
        return
    # set up inb to go outb
    data.outb = data.inb
    client_message = data.inb
    data.inb = b"" # reset inb
    # Handle different client messages
    message_json = json.loads(client_message.decode())
    message = message_json["message"]
    
    response = ""
    # send help info
    if message == "help":
        pass
    # disconnect player
    elif message == "exit":
        message_json = {"message": "Your opponent left the game! You win by default."}
        if sock == X_player:
            O_player.send(json.dumps(message_json).encode())
            game.liveGame = False
            return
        if sock == O_player:
            X_player.send(json.dumps(message_json).encode())
            game.liveGame = False
            return
        pass
    # enter move into game
    elif game.liveGame:
        if sock == X_player:
            response = game.takeTurn(message, "X")
        elif sock == O_player:
            response = game.takeTurn(message, "O")
        response += "\n" + game.getPrintableBoard()
        response_json = {
            "message": response,
            "liveGame": game.liveGame
            }
        X_player.send(json.dumps(response_json).encode())
        O_player.send(json.dumps(response_json).encode())
    else:
        response_json = {"message": "This game is not live. Waiting for opponent"}
        sock.send(json.dumps(response_json).encode())


def close_client_connection(sock, data):
    logger.info(f"[close_client_connection] Closing connection to {data.addr}, client: {clients[sock]}")
    sel.unregister(sock)
    sock.close()
    del clients[sock]
    if sock == X_player or sock == O_player:
        message_json = {"message": "Your opponent left the game! You win by default."}
        for conn in clients:
            conn.send(json.dumps(message_json).encode())
    remove_player(sock)

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
# Main program setup
host = '0.0.0.0'  # Listen on all network interfaces
port = 12350

if len(sys.argv) < 2:
    host = '0.0.0.0'  # Listen on all network interfaces
    port = 12350
else:
    logger.info(f"host: {sys.argv[1]}")
    logger.info(f"port: {sys.argv[2]}")
    host = sys.argv[1]
    port = int(sys.argv[2])

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
