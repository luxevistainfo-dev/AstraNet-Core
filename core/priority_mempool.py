# core/priority_mempool.py

import heapq
from datetime import datetime

class PriorityTransaction:
    def __init__(self, tx, ai_score=0.5, fee=0):
        self.tx = tx
        self.ai_score = ai_score
        self.fee = fee
        self.timestamp = datetime.now()
        self.priority_score = self.calculate_priority()
    
    def calculate_priority(self):
        """Calculate priority based on AI score and fee"""
        return (self.ai_score * 0.7) + (self.fee * 0.3)
    
    def __lt__(self, other):
        return self.priority_score > other.priority_score

class PriorityMempool:
    def __init__(self, max_size=1000):
        self.heap = []
        self.tx_map = {}
        self.max_size = max_size
        print(f"[PRIORITY] Priority mempool created (max: {max_size})")
    
    def add_tx(self, tx, ai_score=0.5, fee=0):
        """Add transaction with priority"""
        if hasattr(tx, 'tx_id') and tx.tx_id in self.tx_map:
            print(f"[PRIORITY] Transaction {tx.tx_id} already exists")
            return False
        
        # If mempool is full, remove lowest priority
        if len(self.heap) >= self.max_size:
            removed = self.remove_lowest_priority()
            if removed:
                print(f"[PRIORITY] Removed low priority TX: {removed.tx.tx_id}")
        
        # Create priority transaction
        priority_tx = PriorityTransaction(tx, ai_score, fee)
        heapq.heappush(self.heap, priority_tx)
        
        # Store in map
        tx_id = getattr(tx, 'tx_id', str(id(tx)))
        self.tx_map[tx_id] = priority_tx
        
        print(f"[PRIORITY] Added TX {tx_id} with score {priority_tx.priority_score:.2f}")
        return True
    
    def remove_lowest_priority(self):
        """Remove lowest priority transaction"""
        if not self.heap:
            return None
        
        # In a max-heap by priority, lowest is at the end
        self.heap.sort(key=lambda x: x.priority_score)
        lowest = self.heap.pop()
        heapq.heapify(self.heap)
        
        tx_id = getattr(lowest.tx, 'tx_id', str(id(lowest.tx)))
        del self.tx_map[tx_id]
        
        return lowest
    
    def get_next_transactions(self, count=10):
        """Get next N highest priority transactions"""
        if not self.heap:
            return []
        
        # Sort by priority (highest first)
        sorted_txs = sorted(self.heap, key=lambda x: x.priority_score, reverse=True)
        result = [ptx.tx for ptx in sorted_txs[:count]]
        
        print(f"[PRIORITY] Returning {len(result)} transactions")
        return result
    
    def print_status(self):
        """Print current mempool status"""
        print("\n=== PRIORITY MEMPOOL STATUS ===")
        print(f"Transactions in mempool: {len(self.heap)}")
        print(f"Available slots: {self.max_size - len(self.heap)}")
        
        if self.heap:
            print("\nTop 5 transactions by priority:")
            sorted_txs = sorted(self.heap, key=lambda x: x.priority_score, reverse=True)
            for i, ptx in enumerate(sorted_txs[:5], 1):
                tx_id = getattr(ptx.tx, 'tx_id', 'N/A')
                print(f"{i}. TX {tx_id[:8]}... - Score: {ptx.priority_score:.2f}")

# Test function
def test_priority_mempool():
    print("\nTesting PriorityMempool class...")
    
    # Create mock transaction class
    class MockTransaction:
        def __init__(self, tx_id):
            self.tx_id = tx_id
            self.sender = f"sender_{tx_id}"
            self.receiver = f"receiver_{tx_id}"
            self.amount = 100
    
    # Create mempool
    mempool = PriorityMempool(max_size=5)
    
    # Add transactions with different priorities
    transactions = [
        (MockTransaction("tx001"), 0.8, 2.0),  # High AI score, high fee
        (MockTransaction("tx002"), 0.3, 5.0),  # Low AI score, very high fee
        (MockTransaction("tx003"), 0.9, 0.5),  # Very high AI score, low fee
        (MockTransaction("tx004"), 0.5, 1.0),  # Medium both
        (MockTransaction("tx005"), 0.1, 0.1),  # Low both
        (MockTransaction("tx006"), 0.7, 3.0),  # Should replace lowest
    ]
    
    for tx, ai_score, fee in transactions:
        mempool.add_tx(tx, ai_score, fee)
    
    # Print status
    mempool.print_status()
    
    # Get top transactions
    top_txs = mempool.get_next_transactions(3)
    print(f"\nGot {len(top_txs)} top transactions")
    
    print("\nTest completed!")

if __name__ == "__main__":
    test_priority_mempool()
