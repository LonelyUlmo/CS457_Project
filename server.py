import sys
import socket
import selectors
import types
import logging
import json

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(message)s',
    handlers=[
        logging.FileHandler("server.log", mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger()

sel = selectors.DefaultSelector()

client_count = 0

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Accept the connection
    logger.info(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, outb=b"")
    sel.register(conn, selectors.EVENT_READ | selectors.EVENT_WRITE, data=data)
    clientID = get_new_client_ID()
    clients[conn] = clientID
    welcome_message = {
        "message": "Connection Accepted.",
        "clientID": clientID
        }
    conn.send(json.dumps(welcome_message).encode())

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(4096)  # Receive data
        if recv_data:
            logger.info(f"Received \"{recv_data.decode()}\" from {data.addr}")
            data.outb += recv_data  # Prepare to echo data back
        else:
            close_client_connection(sock, data)
    if mask & selectors.EVENT_WRITE and data.outb:
        handle_client_message(sock, data)

def get_new_client_ID():
    global client_count
    new_ID = client_count
    client_count += 1
    return new_ID

def handle_client_message(sock, data):
    logger.info(f"Echoing {repr(data.outb)} to {data.addr}")
    sent = sock.send(data.outb)  # Echo data
    data.outb = data.outb[sent:]  # Keep the part of message that hasn't been sent

def close_client_connection(sock, data):
    logger.info(f"Closing connection to {data.addr}, client: {clients[sock]}")
    sel.unregister(sock)
    sock.close()
    del clients[sock]

# Main program setup
host = '0.0.0.0'  # Listen on all network interfaces
port = 12358

# Set up the listening socket and register it with the selector
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen() # Could alter this to accept a set number of connections
logger.info(f"Listening on {(host, port)}")
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

# Keep track of clients
clients = {}

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
