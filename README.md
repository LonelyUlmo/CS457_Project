# CS457_Project
This project is to recreate the game Othello over a network.

**Author**
Jonathan Evans

It will include a server and two clients. More information will be updated as the project 
is fleshed out.

## **Current Functionality:**
Run this command to start the server:
    python3 server.py 0.0.0.0 12345

Run this command to have a client connect to the server:
    python3 client.py 0.0.0.0 12345 "join_game" 123

## **How to play:**
...
## **Technologies used:**
...
## **Additional Resources:**
...

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