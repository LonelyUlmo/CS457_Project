import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()

def start_connections(host, port):
    server_addr = (host, port)
    print("starting connection to", server_addr)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(server_addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    data = types.SimpleNamespace(
        inb=b"",
        outb=b"")
    sel.register(sock, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(4096)
        if recv_data:
            print("received", repr(recv_data))
        else:
            close_connection(sock)
    if mask & selectors.EVENT_WRITE:
        send_message(sock, data)

def close_connection(sock):
    print("closing connection")
    sel.unregister(sock)
    sock.close()

def send_message(sock, data):
    message = input("Enter Message Here: ")
    print("Current value of data.outb is:", data.outb)
    # Exit condition
    if message == "exit":
        close_connection(sock)
        return
    # Send the message
    if data.outb == message: # reset outb value if the whole message has been sent
        data.outb = b""
    if not data.outb:
        data.outb = message.encode("utf-8")
    if data.outb:
        print("sending", repr(data.outb))
        sent = sock.send(data.outb)  # Should be ready to write
        data.outb = data.outb[sent:]

# main program
host = '129.82.45.121' # this is the IP address of the blowfish machine (I hope this doesn't change periodically. Idk how to find it other than running the 'hostname -I' command on the host machine)
port = 12358
sock = start_connections(host, port)

# the event loop
try:
    while True:
        events = sel.select(timeout=1)
        if events:
            for key, mask in events:
                service_connection(key, mask)
        # Check for a socket being monitored to continue.
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()
