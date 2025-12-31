import time
import hashlib

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = time.time()
        self.tx_id = self.calculate_hash()

    def calculate_hash(self):
        raw = f"{self.sender}{self.receiver}{self.amount}{self.timestamp}"
        return hashlib.sha256(raw.encode()).hexdigest()
