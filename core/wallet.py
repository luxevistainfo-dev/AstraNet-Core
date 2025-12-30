class Wallet:
    def __init__(self, owner):
        self.owner = owner
        self.balance = 0
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return True
        return False
