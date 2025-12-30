import hashlib
import time

class Block:
    def __init__(self, index, transactions, prev_hash):
        self.index = index
        self.transactions = transactions
        self.prev_hash = prev_hash
        self.timestamp = time.time()
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        raw = f"{self.index}{self.transactions}{self.prev_hash}{self.timestamp}"
        return hashlib.sha256(raw.encode()).hexdigest()
