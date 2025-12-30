# ai/node_health.py
import json
from datetime import datetime

class NodeHealthMonitor:
    def __init__(self, node_id="node_01"):
        self.node_id = node_id
        self.health_history = []
    
    def run_check(self, latest_block_time=None):
        # Simulated metrics
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'cpu': {'percent': 45.5},
            'memory': {'percent': 60.2},
            'disk': {'percent': 75.8},
            'network': {'latency_ms': 25.3}
        }
        
        sync_status = {
            'synced': True,
            'lag_seconds': 2.5
        }
        
        health_score = {
            'overall_score': 85.5,
            'health_status': 'HEALTHY',
            'component_scores': {
                'cpu': 85.5,
                'memory': 85.5,
                'disk': 85.5,
                'network': 85.5,
                'sync': 85.5
            }
        }
        
        health_record = {
            'timestamp': datetime.now().isoformat(),
            'node_id': self.node_id,
            'metrics': metrics,
            'sync_status': sync_status,
            'health_score': health_score,
            'alerts': []
        }
        
        self.health_history.append(health_record)
        return health_record
    
    def print_health_status(self):
        print("\n=== NODE HEALTH STATUS ===")
        if not self.health_history:
            print("No health data available")
            return
        
        latest = self.health_history[-1]
        print(f"Health score: {latest['health_score']['overall_score']}/100")
        print(f"CPU: {latest['metrics']['cpu']['percent']}%")
        print(f"Memory: {latest['metrics']['memory']['percent']}%")
        print(f"Disk: {latest['metrics']['disk']['percent']}%")

def test_node_health():
    print("Testing NodeHealthMonitor...")
    monitor = NodeHealthMonitor("test_node")
    
    health_record = monitor.run_check()
    print(f"Health score: {health_record['health_score']['overall_score']}")
    
    monitor.print_health_status()
    print("Test completed!")

if __name__ == "__main__":
    test_node_health()
