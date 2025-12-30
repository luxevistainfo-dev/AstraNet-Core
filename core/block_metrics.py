# core/block_metrics.py
import json
from datetime import datetime

class BlockMetrics:
    def __init__(self, metrics_file="block_metrics.json"):
        self.metrics_file = metrics_file
        self.block_history = []
    
    def analyze_block(self, block, mempool_size=0):
        tx_count = len(block.transactions) if hasattr(block, 'transactions') else 0
        total_amount = sum(getattr(tx, 'amount', 0) for tx in block.transactions) if hasattr(block, 'transactions') else 0
        
        metrics = {
            'block_id': getattr(block, 'id', 'unknown'),
            'timestamp': datetime.now().isoformat(),
            'tx_count': tx_count,
            'total_amount': total_amount,
            'avg_tx_value': total_amount / tx_count if tx_count > 0 else 0
        }
        
        self.block_history.append(metrics)
        return metrics
    
    def get_active_alerts(self):
        """Get active alerts (empty for now)"""
        return []
    
    def print_dashboard(self):
        print("\n=== BLOCK METRICS DASHBOARD ===")
        if not self.block_history:
            print("No block data available")
            return
        
        print(f"Total blocks analyzed: {len(self.block_history)}")
        print(f"Last block: {self.block_history[-1]['block_id']}")
        
        # Add this line to prevent errors
        print("✅ Dashboard generated successfully")

def test_block_metrics():
    print("Testing BlockMetrics...")
    class MockBlock:
        def __init__(self):
            self.id = "test_block"
            self.transactions = []
    
    metrics = BlockMetrics()
    block = MockBlock()
    result = metrics.analyze_block(block)
    print(f"Analyzed block: {result}")
    metrics.print_dashboard()
    print("Test completed!")

if __name__ == "__main__":
    test_block_metrics()
