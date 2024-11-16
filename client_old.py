import sys
import socket
import selectors
import struct
import traceback

import libclient

sel = selectors.DefaultSelector()

def create_request(action, value):
    if action == "start":
        return dict( # TODO: this is a temporary holder. Decide whther to use utf-8 or binary coding
            type="text/json",
            encoding="utf-8",
            content=dict(action=action, value=value),
        )
    elif action == "search":
        return dict( # TODO: this is a temporary holder. Decide whther to use utf-8 or binary coding
            type="text/json",
            encoding="utf-8",
            content=dict(action=action, value=value),
        )
    return dict( # default send
        type="binary/custom-client-binary-type",
        encoding="binary",
        content=bytes(action + value, encoding="utf-8"),
    )

def start_connection(host, port, request):
    addr = (host, port)
    print("starting connection to", addr)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    message = libclient.Message(sel, sock, addr, request)
    sel.register(sock, events, data=message)


if len(sys.argv) != 5:
    print("usage:", sys.argv[0], "<host> <port> <action> <value>")
    print("This will be updated for Othello functionality soon.")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
action, value = sys.argv[3], sys.argv[4]
request = create_request(action, value)
start_connection(host, port, request)

try:
    while True:
        events = sel.select(timeout=1)
        for key, mask in events:
            message = key.data
            try:
                message.process_events(mask)
            except Exception:
                print(
                    "main: error: exception for",
                    f"{message.addr}:\n{traceback.format_exc()}",
                )
                message.close()
        # Check for a socket being monitored to continue.
        if not sel.get_map():
            break
        # Code to keep the connection open
        # After processing events, ask the user if they want to send another message
        user_input = input("Send another message? (y/n): ").strip().lower()
        if user_input == 'y':
            # new_action = input("Enter the new action: ").strip()
            # new_value = input("Enter the new value: ").strip()
            new_action = "join_game"
            new_value = ""
            new_request = create_request(new_action, new_value)
            message.request = new_request  # Update the request in the message object
            message._request_queued = False  # Reset the flag to queue the new request
            message._set_selector_events_mask("rw")  # Prepare to send the new message
        else:
            print("Closing connection...")
            message.close()
            break
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()