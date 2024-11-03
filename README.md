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