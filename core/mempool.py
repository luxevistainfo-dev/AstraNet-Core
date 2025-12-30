class Mempool:
    def __init__(self):
        self.transactions = []
    
    def add_tx(self, tx):
        self.transactions.append(tx)
    
    def clear(self):
        self.transactions = []
