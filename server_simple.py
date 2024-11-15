import sys
import socket
import selectors
import types
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("server.log"),
                        logging.StreamHandler(sys.stdout)
                    ])

sel = selectors.DefaultSelector()

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Accept the connection
    logging.info(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, outb=b"")
    sel.register(conn, selectors.EVENT_READ | selectors.EVENT_WRITE, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(4096)  # Receive data
        if recv_data:
            logging.info(f"Received \"{recv_data.decode()}\" from {data.addr}")
            data.outb = recv_data  # Prepare to echo data back
        else:
            close_connection(sock, data)

    if mask & selectors.EVENT_WRITE and data.outb:
        logging.info(f"Echoing {repr(data.outb)} to {data.addr}")
        sent = sock.send(data.outb)  # Echo data
        data.outb = data.outb[sent:]  # Clear sent data

def close_connection(sock, data):
    logging.info(f"Closing connection to {data.addr}")
    sel.unregister(sock)
    sock.close()

# Main program setup
host = '0.0.0.0'  # Listen on all network interfaces
port = 12358

# Set up the listening socket and register it with the selector
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
logging.info(f"Listening on {(host, port)}")
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

# Main event loop
try:
    while True:
        for key, mask in sel.select(timeout=None):
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    logging.info("Caught keyboard interrupt, exiting")
finally:
    sel.close()
