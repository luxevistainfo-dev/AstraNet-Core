# core/history.py

import json
from datetime import datetime

class TxHistory:
    def __init__(self, log_file="tx_history.json"):
        self.log_file = log_file
        self.all_txs = []
        self.load_history()
    
    def log_tx(self, tx):
        """Log transaction to history"""
        tx_record = {
            "id": getattr(tx, 'tx_id', str(id(tx))),
            "sender": getattr(tx, 'sender', 'unknown'),
            "receiver": getattr(tx, 'receiver', 'unknown'),
            "amount": getattr(tx, 'amount', 0),
            "timestamp": getattr(tx, 'timestamp', datetime.now().isoformat()),
            "log_time": datetime.now().isoformat()
        }
        
        self.all_txs.append(tx_record)
        self.save_history()
        print(f"[HISTORY] Transaction logged: {tx_record['id']}")
        return tx_record
    
    def save_history(self):
        """Save history to JSON file"""
        try:
            with open(self.log_file, 'w') as f:
                json.dump(self.all_txs[-1000:], f, indent=2)
        except Exception as e:
            print(f"[ERROR] Saving history: {e}")
    
    def load_history(self):
        """Load history from JSON file"""
        try:
            with open(self.log_file, 'r') as f:
                self.all_txs = json.load(f)
            print(f"[HISTORY] Loaded {len(self.all_txs)} transactions")
        except FileNotFoundError:
            print("[HISTORY] No previous history found")
            self.all_txs = []
        except json.JSONDecodeError:
            print("[HISTORY] Corrupted history file, starting fresh")
            self.all_txs = []
    
    def print_stats(self):
        """Print statistics about transaction history"""
        print("\n=== TRANSACTION HISTORY STATS ===")
        print(f"Total transactions: {len(self.all_txs)}")
        if self.all_txs:
            print(f"Last transaction: {self.all_txs[-1]['timestamp']}")
            print(f"First transaction: {self.all_txs[0]['timestamp']}")

# Test function
def test_history():
    print("\nTesting TxHistory class...")
    history = TxHistory("test_history.json")
    
    # Create a mock transaction
    class MockTx:
        def __init__(self):
            self.tx_id = "test_tx_123"
            self.sender = "alice"
            self.receiver = "bob"
            self.amount = 100
            self.timestamp = datetime.now().isoformat()
    
    # Log some transactions
    for i in range(5):
        tx = MockTx()
        tx.tx_id = f"test_tx_{i}"
        history.log_tx(tx)
    
    history.print_stats()
    print("Test completed!")

if __name__ == "__main__":
    test_history()

