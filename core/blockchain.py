import time
import hashlib

class Block:
    def __init__(self, index, previous_hash, transactions, nonce=0, hash=""):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = hash

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4

    def create_genesis_block(self):
        return Block(0, "0", [], 0, "0")

    def mine_block(self, transactions):
        last_block = self.chain[-1]
        nonce = 0
        while True:
            content = f"{last_block.hash}{transactions}{nonce}"
            hash_try = hashlib.sha256(content.encode()).hexdigest()
            if hash_try.startswith("0" * self.difficulty):
                new_block = Block(
                    index=last_block.index + 1,
                    previous_hash=last_block.hash,
                    transactions=transactions,
                    nonce=nonce,
                    hash=hash_try
                )
                self.chain.append(new_block)
                return new_block
            nonce += 1
