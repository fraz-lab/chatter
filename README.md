# Chatter WebSocket Chat Server

https://github.com/user-attachments/assets/eb5f5c2a-f574-44b3-b979-abc2e05a9d7f

https://github.com/user-attachments/assets/eb5f5c2a-f574-44b3-b979-abc2e05a9d7f" 




A simple **FastAPI WebSocket-based chat server** with **user authentication** from a `users.json` file and basic **chat history** support.

---

## 📂 Project Structure

```
chatter/
│
├── chat_server.py     # Main server script
├── users.json         # User credentials (JSON file)
├── run_server.bat     # Windows batch file to start server
└── README.md
```

---

## ⚙️ Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/chatter.git
   cd chatter
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate    # On Windows
   source .venv/bin/activate # On Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install fastapi uvicorn
   ```

---

## 👤 User Authentication

The server uses a `users.json` file for login.  
Create a `users.json` file in the root directory with the following structure:

```json
{
  "test1": "pass1",
  "test2": "pass2"
}
```

- **Key** = Username  
- **Value** = Password

You can add as many users as you need.

---

## 🚀 Run the Server

### Option 1: Run with Python
```bash
python chat_server.py
```

The server will start at:  
👉 `http://0.0.0.0:8000/ws/chat`

### Option 2: Run with Batch File (Windows)

Use the provided `run_server.bat` file to quickly start the server.

**run_server.bat**
```bat
@echo off
ECHO Activating virtual environment...
CALL .venv\Scripts\activate
ECHO Starting Chat Server...
python chat_server.py
pause
```

Run it by double-clicking the file.

---

## 💬 How It Works

1. Client connects to **WebSocket endpoint**:  
   ```
   ws://localhost:8000/ws/chat
   ```

2. The first message must include authentication info:
   ```json
   {
     "username": "test1",
     "password": "pass1"
   }
   ```

   - If credentials are valid → `{ "auth": "ok" }`
   - If invalid → `{ "error": "invalid credentials" }`

3. After login:
   - The server sends **chat history** to the client.
   - Any new messages are broadcast to other connected users.

4. Message format:
   ```json
   {
     "thread": "test1",
     "message": "Hello World!",
     "from": "test1"
   }
   ```

---





## 📝 Notes
- Chat history is **stored in memory only** (resets when server restarts).  
- Multi-user support with authentication.  
- You can expand it to store chat history in a database if needed.  

---
