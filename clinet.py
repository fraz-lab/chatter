import asyncio
import json
import websockets
import getpass
from pathlib import Path

from textual.app import App, ComposeResult
from textual.widgets import Static, TextLog, Input
from textual.containers import Horizontal, Vertical
from textual import events
 

CONFIG_FILE = Path("config.json")

with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    config = json.load(f)

SERVER_WS_URL = f"ws://{config['server']['host']}:{config['server']['port']}/ws/chat"
class ChatPane(TextLog):
    def __init__(self, thread_key: str):
        super().__init__()
        self.thread_key = thread_key
 
    def add_message(self, sender: str, message: str):
        self.write("")
        self.write(f"[{sender}] {message}")
 
class TwoPaneChatApp(App):
    CSS = """
    Horizontal       { height: 85%; }
    Vertical         { width: 1fr; height: 100%; }
    .header          { height: 3; content-align: center middle; text-style: bold; background: $accent-lighten-1; }
    TextLog          { border: green; height: 75%; padding: 1; overflow-y: auto; }
    Input            { border: blue; height: 12%; }
    """
 
    def __init__(self, username: str, password: str, **kwargs):
        super().__init__(**kwargs)
        self.USERNAME = username
        self.PASSWORD = password
        self.ws = None
 
    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical():
                yield Static(" Test 1 ", classes="header")
                self.chat1 = ChatPane("test1")
                yield self.chat1
                self.input1 = Input(placeholder="Type for Test 1")
                yield self.input1
 
            with Vertical():
                yield Static(" Test 2 ", classes="header")
                self.chat2 = ChatPane("test2")
                yield self.chat2
                self.input2 = Input(placeholder="Type for Test 2")
                yield self.input2
 
    async def on_mount(self):
        try:
            self.ws = await websockets.connect(SERVER_WS_URL)
            await self.ws.send(json.dumps({
                "password": self.PASSWORD,
                "username": self.USERNAME
            }))
            raw = await self.ws.recv()
            data = json.loads(raw)
        except Exception as e:
            self.chat1.write(f"[ERROR] Connection failed: {e}")
            return
 
        if data.get("error"):
            self.chat1.write(f"[SERVER] {data['error']}")
            await self.action_quit()
            return
 
        self.set_interval(0.1, self.receive_messages)
        self.input1.focus()
 
    async def receive_messages(self):
        if not self.ws:
            return
        try:
            raw = await asyncio.wait_for(self.ws.recv(), timeout=0.01)
            data = json.loads(raw)
        except asyncio.TimeoutError:
            return
        except websockets.ConnectionClosed:
            await self.action_quit()
            return
 
        thread = data.get("thread")
        sender = data.get("sender")
        msg = data.get("message")
 
        if thread == "test1":
            self.chat1.add_message(sender, msg)
        elif thread == "test2":
            self.chat2.add_message(sender, msg)
 
    async def handle_input(self, thread_key: str, input_widget: Input):
        text = input_widget.value.strip()
        if not text:
            return
        payload = {
            "thread": thread_key,
            "sender": self.USERNAME,
            "message": text
        }
        await self.ws.send(json.dumps(payload))

        # 👇 Local echo so you see your own messages immediately
        if thread_key == "test1":
            self.chat1.add_message(self.USERNAME, text)
        elif thread_key == "test2":
            self.chat2.add_message(self.USERNAME, text)

        input_widget.value = ""
        input_widget.focus()
    async def on_input_submitted(self, event: Input.Submitted):
        if event.input is self.input1:
            await self.handle_input("test1", self.input1)
        elif event.input is self.input2:
            await self.handle_input("test2", self.input2)
 
    async def on_key(self, event: events.Key):
        if event.key == "tab":
            if self.focused is self.input1:
                self.input2.focus()
            else:
                self.input1.focus()
            event.stop()
        elif event.key == "1":
            self.input1.focus()
            event.stop()
        elif event.key == "2":
            self.input2.focus()
            event.stop()
 
    async def on_unmount(self):
        if self.ws:
            await self.ws.close()
 
# ─ Authentication ──────────────────────────────────────────────────────
async def try_auth(password: str, username: str) -> bool:
    try:
        ws = await websockets.connect(SERVER_WS_URL)
        await ws.send(json.dumps({"password": password, "username": username}))
        raw = await asyncio.wait_for(ws.recv(), timeout=2.0)
        data = json.loads(raw)
        await ws.close()
 
        if data.get("auth") == "ok":
            return True
        return False
    except Exception as e:
        print(f"Exception: {e}")
        return False
 
def main():
    while True:
        pwd = getpass.getpass("Password: ")
        user = input("Username: ")
        if asyncio.run(try_auth(pwd, user)):
            break
        print("❌ Authentication failed — try again.\n")
 
    TwoPaneChatApp(user, pwd).run()
 
if __name__ == "__main__":
    main()