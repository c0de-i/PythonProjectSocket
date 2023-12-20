import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Socket successfully created")
    server_ip = "192.168.10.49"
    port = 8080
    s.bind((server_ip, port))
    print("Socket binded to %s" % (port))
    print("Server IP address:", socket.gethostbyname(socket.gethostname()))
    s.listen(5)
    print("Socket is listening")

    while True:
        c, addr = s.accept()
        print("Got connection from", addr)
        data = c.recv(4096)
        print(data.decode())
