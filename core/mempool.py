class Mempool:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, tx):
        self.transactions.append(tx)
