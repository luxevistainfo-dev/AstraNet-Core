import time
import hashlib

class Block:
    def __init__(self, index, previous_hash, transactions, nonce, hash):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = hash

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0", [], 0, "0")

    def mine_block(self, difficulty=4):
        last_block = self.chain[-1]
        nonce = 0
        while True:
            content = f"{last_block.hash}{nonce}"
            hash_try = hashlib.sha256(content.encode()).hexdigest()
            if hash_try.startswith("0"*difficulty):
                return nonce, hash_try
            nonce += 1
