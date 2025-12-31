import socket
import threading

class Node:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen()
        print(f"Node running on {self.host}:{self.port}")
        while True:
            conn, addr = server.accept()
            data = conn.recv(4096)
            print("Received from", addr, ":", data.decode())
            conn.close()
