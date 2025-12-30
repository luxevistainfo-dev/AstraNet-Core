# core/dynamic_block.py
from datetime import datetime
import json

class DynamicBlockSize:
    def __init__(self, min_size=1, max_size=10, base_size=2):
        self.min_size = min_size
        self.max_size = max_size
        self.base_size = base_size
        self.history = []
    
    def calculate_block_size(self, mempool, network_load=0.5):
        if hasattr(mempool, 'transactions'):
            tx_count = len(mempool.transactions)
        else:
            tx_count = 0
        
        mempool_factor = min(tx_count / 100, 1.0)
        network_factor = network_load
        
        dynamic_size = self.base_size * (1 + (mempool_factor * 0.4) + (network_factor * 0.3))
        final_size = int(round(dynamic_size))
        final_size = max(self.min_size, min(self.max_size, final_size))
        
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'size': final_size,
            'mempool_size': tx_count
        })
        
        return final_size
    
    def get_statistics(self):
        if not self.history:
            return None
        sizes = [h['size'] for h in self.history]
        return {
            'current': sizes[-1] if sizes else self.base_size,
            'average': sum(sizes) / len(sizes),
            'history': self.history[-5:]
        }

def test_dynamic_block():
    print("Testing DynamicBlockSize...")
    class MockMempool:
        def __init__(self, size):
            self.transactions = ['tx'] * size
    
    calculator = DynamicBlockSize()
    sizes = [5, 50, 150]
    
    for size in sizes:
        mempool = MockMempool(size)
        block_size = calculator.calculate_block_size(mempool)
        print(f"Mempool: {size} -> Block size: {block_size}")
    
    print("Test completed!")

if __name__ == "__main__":
    test_dynamic_block()
