# server.py
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

app = FastAPI()

# hardcoded users
VALID_USERS = {"admin": "1234", "user": "pass"}

# track connections
connections: list[WebSocket] = []

# in-memory chat history
chat_history = {"test1": [], "test2": []}

@app.websocket("/ws/chat")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        # wait for auth packet
        raw = await ws.receive_text()
        data = json.loads(raw)
        username = data.get("username")
        password = data.get("password")

        if username not in VALID_USERS or VALID_USERS[username] != password:
            await ws.send_text(json.dumps({"error": "invalid credentials"}))
            await ws.close()
            return

        # auth success
        await ws.send_text(json.dumps({"auth": "ok"}))
        connections.append(ws)

        # send history to new client
        for thread, msgs in chat_history.items():
            for m in msgs:
                await ws.send_text(json.dumps(m))

        # main chat loop
        while True:
            raw = await ws.receive_text()
            msg = json.loads(raw)

            # save to history
            thread = msg.get("thread")
            if thread in chat_history:
                chat_history[thread].append(msg)

            # broadcast to others (NOT the sender)
            for conn in connections:
                if conn != ws:
                    try:
                        await conn.send_text(json.dumps(msg))
                    except:
                        pass

    except WebSocketDisconnect:
        if ws in connections:
            connections.remove(ws)
