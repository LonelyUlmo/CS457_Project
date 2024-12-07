# CS457_Project
This project simulates a game Tic Tac Toe over a network.

**Author**
Jonathan Evans

## **Current Functionality:**
This program allows two clients to connect to a server and play a game of Tic Tac Toe.

Restarting a Game:
    The game doesn't handle starting a second game properly, so the server should be reset before each game.

Logs:
    When the server terminates, the logs will be saved under serverLogs.log

## **How to play:**
To start the server and connect as a client, follow these instructions.

Running the client:
    python3 server.py 0.0.0.0 <port-number>
    example: python3 server.py 0.0.0.0 12345

Running the server:
    `python3 client.py <server-IP> <port-number>`
    example: `python3 client.py 129.82.45.121 12345` (if server is on cs blowfish machine)

Gameplay:
    Once the game has started, you can enter in a tile location as your move, 'A1' for example will let you mark the A1 tile.
    Once the board is full or a player has one, the game will be over!
    If a client misenters their input, the server will inform them of the missinput and ask the client to try again.

Exitting a game:
    A client can quit the game at any time by sending `exit`.

## **Sprint Notes**
10.5.2024 - Sprint 1 complete.
- server can handle multiple connections and keep them open.
- client can have a continuous conversation with the server.
- requirements.txt now included.

11.3.2024 - Sprint 2/3:
- Issue keeping connection open (the server closes the connection with the client after responding once.)
- Might need to refactor the Message class:
    - I'm unsure if this class can handle multiple connections and keep those connections open.
    - Hopefully, I can just change how it opens and closes connections.
- Implemented first draft of Othello Game model:
    - It has a board and can update the board. (I'll want to have the server send an updated board-state to the clients after each player-turn.)
    - It now simulates turns
- TODO:
    - Othello game needs to handle:
        - moves that are out of bounds
        - _updateInDirection() needs to stop at the walls.
        - detect end of game
        - detect case where player has no valid moves, so they forfit their turn.
    - Logging
    - Configure client/server connections, keep them open, and enable "conversations"(multiple messages being sent back and forth)
    - Update game-state from server to all clients

11.13.2024
- Today, I'm practically starting over from the beginning. I'm going to try to get a chatroom set up between the client and server on client_simple.py and server_simple.py.
- I realized that the server is set to '0.0.0.0', but the client needs the IP address of the host machine. I found the IP address of the blowfish machine with this terminal comand: 'hostname -I'. From here on, we'll keep blowfish as the host machine and hope the IP address doesn't change.
- I'm not trying to get the client to be able to send message multiple times. I have made an attempt at this and having the server reciece multiple messages from the client.
- I'm running into an error: when the client sends a second message, it gets the first message echoed back from the server. I'm not sure if this is a bug in the client or the server. I'm thinking of asking the professor for help. It would be a good checkpoint for me to catch up with him.

11.14.2024
- Proffessor Haefner gave me some client code to help me simplify things down. I've also simplified the server code and implemented logging on the server side.
- I was having some bugs with the logging, so I tweaked the code a bit. It now is set to "w" mode which overwrites any previous file.

11.16.2024
- Removed some redundant files and renamed some other files.

11.25.2024
- Switching to Tic Tac Toe so the game logic isn't to difficult to figure out.
- I've got the Tic Tac Toe game logic written.
- I need to figure out how clients are going to be both listening to the server and listening for user input.
- I need to figure out how the server will concurrently handle game logic, listening to clients, and messaging clients.
- I'm having these weird residual issues with the logs. I think the TicTacToe class having a copy of the logger is causing issues. I'm going to copy it into the server.py file for simplicity.
- I'm not sure what is up with the logs. Might have to come back to it later.
- Next, I need to bootstrap getting two clients to play a game of tic tac toe. Can refine the process once I get that done.

11.26.2024
- Now assigns players a team when they connect.
- Now begins a game once two players are connected
- Sends the game board to the players
- TODO:
    - have client handle game board message and user input.

11.27.2024
- New protocol: make the client as dumb as possible.
    - The client now only does two things:
        - Prints whatever the server sends to it (everything will be in a json with a "message" varriable. It prints the message.)
        - Sends whatever input the user types into the terminal to ther server.
    - The server will handle all the game logic as well as format the messages to be displayed client-side.

11.28.2024
- Got the game to work between two clients! Handles a whole game.
- Handles players leavingearly.
- Handles extra players trying to join. Kicks them.
- Full game can be played
- TODO:
    - Write "help" response
    - Accept command line args for host and port
    - Update requriements.txt
    - Server doesn't reset after a game has terminated.

12.2.2024
- Accepts command line arguments
