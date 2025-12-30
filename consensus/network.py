import socket
import threading

nodes = []

def connect_node(ip, port):
    s = socket.socket()
    s.connect((ip, port))
    nodes.append(s)

def broadcast_tx(tx_data):
    for node in nodes:
        node.send(tx_data.encode())

def start_server(port):
    s = socket.socket()
    s.bind(("", port))
    s.listen()
    print("Listening on port", port)
    while True:
        client, addr = s.accept()
        data = client.recv(1024).decode()
        print("Received:", data)
