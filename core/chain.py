from core.block import Block

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis()
    
    def create_genesis(self):
        genesis = Block(0, [], "0")
        self.chain.append(genesis)
    
    def add_block(self, transactions):
        prev = self.chain[-1]
        block = Block(len(self.chain), transactions, prev.hash)
        self.chain.append(block)
