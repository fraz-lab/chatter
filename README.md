**Chatter – FastAPI WebSocket Chat (with Textual Client)**

Chatter is a two-pane chat application built with:

FastAPI + WebSockets for the server

Textual (TUI) for the client

JSON configuration for users and server host/port

It’s a simple but extendable example of real-time messaging in Python.


📂 Project Structure
chatter/
│── server.py        # FastAPI WebSocket server
│── client.py        # Textual client (two-pane chat)
│── config.json      # Server & user configuration
│── run_server.bat   # Windows batch script to start server
│── run_client.bat   # Windows batch script to start client
│── README.md        # Documentation

⚙️ Configuration (config.json)

All settings are stored in a JSON file.

Example:

{
  "server": {
    "host": "0.0.0.0",
    "port": 8000
  },
  "users": {
    "admin": "1234",
    "user": "pass",
    "alice": "wonderland"
  }
}


host: Set to 0.0.0.0 to accept connections from all devices on your network.

port: Port number (default: 8000).

users: Dictionary of username: password pairs.

👉 To add new users, simply edit this file.

🚀 How It Works

Server (server.py)

Reads config.json for valid users and server info.

Accepts WebSocket connections at /ws/chat.

Authenticates with username/password.

Keeps in-memory chat history per thread (test1 and test2).

Broadcasts messages to all other connected clients.

Client (client.py)

Reads config.json to know which server to connect to.

Prompts for username and password.

Opens two chat panes (Test 1 and Test 2).

Messages you send appear locally and are broadcasted to other clients.

Keyboard shortcuts:

TAB → switch between inputs

1 → focus Test 1

2 → focus Test 2

▶️ Running the Project
1. Install Dependencies

Make sure you are in a virtual environment (.venv) and run:

pip install fastapi uvicorn websockets textual

2. Start the Server

Either run manually:

python server.py


Or use the provided run_server.bat:

@echo off
ECHO Starting Chatter Server...
CALL .venv\Scripts\activate
python server.py
pause

3. Start the Client

Run manually:

python client.py


Or use run_client.bat:

@echo off
ECHO Starting Chatter Client...
CALL .venv\Scripts\activate
python client.py
pause

🧪 Example Flow

Start the server:

uvicorn running on http://0.0.0.0:8000


Run the client:

Username: admin
Password: ****


Two panes (Test 1, Test 2) open in your terminal.

Start chatting – multiple clients on the same LAN can connect.

✨ Features

✅ Multiple users from config.json

✅ Two chat rooms (test1, test2)

✅ Authentication via JSON config

✅ Real-time broadcasting

✅ Simple .bat scripts for one-click run

🔮 Roadmap

Persistent chat history (save to file/db)

Multiple dynamic chat rooms

Auto-reload config.json without restart
