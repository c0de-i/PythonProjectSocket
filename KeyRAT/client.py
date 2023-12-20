import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_ip = '192.168.10.49'
port = 8080
s.connect((server_ip,port))
s.close()