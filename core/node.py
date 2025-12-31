import time

class Node:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.running = False

    def start(self):
        self.running = True
        print(f"Node running on {self.ip}:{self.port}")
        while self.running:
            time.sleep(1)
