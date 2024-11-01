import sys
import socket
import selectors
import traceback

import libserver

sel = selectors.DefaultSelector()

def accept_wrapper(sock):
    conn, addr = sock.accept() # Should be ready to read
    print("accepted connection from", addr)
    conn.setblocking(False)
    message = libserver.Message(sel, conn, addr)
    sel.register(conn, selectors.EVENT_READ, data=message)

if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Avoid bind() exception: OSError: [Errno 48] Address already in use
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Note: This helps to avoid the "Address already in use" error.
lsock.bind((host, port))
lsock.listen()
print("listening on", (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

# players = { connection_1, connection_2 }
# How many players exist:
#   if 1: 
#       "Waiting for an opponent..."
#   if 2:
#       "Opponent found! Game Beginning:"
# Drop any extra players:
#   "Game room is already full. Find another server."

try:
    while True:
        events = sel.select(timeout=None) # TODO: can this handle multiple connections?
        # make sure that any methods that should only be called once are either checking a state variable themselves, 
        # or the state variable set by the method is checked by the caller.
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                message = key.data
                try:
                    message.process_events(mask) # What happens if this is called multiple times on the same connection?
                                                 # It may only work the first time.
                except Exception:
                    print(
                        "main: error: exception for",
                        f"{message.addr}:\n{traceback.format_exc()}",
                    )
                    message.close()
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()