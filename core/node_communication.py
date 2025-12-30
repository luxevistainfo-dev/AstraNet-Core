# core/node_communication.py

import json
import logging
from datetime import datetime
from collections import deque
import threading
import time

class NodeCommunicationLog:
    def __init__(self, log_file="node_comm.log", max_entries=10000):
        self.log_file = log_file
        self.comm_log = deque(maxlen=max_entries)
        self.message_count = 0
        self.lock = threading.Lock()
        
        # Setup logging
        self.setup_logging()
        
        print(f"[COMM-LOG] Communication log initialized")
        print(f"[COMM-LOG] Log file: {log_file}")
        print(f"[COMM-LOG] Max entries: {max_entries}")
    
    def setup_logging(self):
        """Setup file and console logging"""
        self.logger = logging.getLogger('node_communication')
        self.logger.setLevel(logging.INFO)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # File handler
        file_handler = logging.FileHandler(self.log_file)
        file_format = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        self.logger.addHandler(file_handler)
        
        # Console handler (optional)
        console_handler = logging.StreamHandler()
        console_format = logging.Formatter(
            '[COMM] %(asctime)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)
    
    def log_message(self, sender, receiver, message_type, message_data, direction="outgoing"):
        """
        Log a communication message between nodes
        
        Args:
            sender: ID of the sending node
            receiver: ID of the receiving node
            message_type: Type of message (e.g., "block_proposal", "transaction", "sync_request")
            message_data: The actual message data
            direction: "outgoing" or "incoming"
        """
        with self.lock:
            self.message_count += 1
            
            log_entry = {
                "id": self.message_count,
                "timestamp": datetime.now().isoformat(),
                "sender": sender,
                "receiver": receiver,
                "type": message_type,
                "direction": direction,
                "data_size": len(str(message_data)),
                "data": message_data if isinstance(message_data, (str, int, float, bool, list, dict)) else str(message_data)
            }
            
            # Add to memory log
            self.comm_log.append(log_entry)
            
            # Log to file
            log_message = f"{direction.upper()} {sender} -> {receiver}: {message_type}"
            self.logger.info(log_message)
            
            return log_entry
    
    def log_block_proposal(self, sender, receiver, block_data):
        """Log a block proposal message"""
        return self.log_message(
            sender=sender,
            receiver=receiver,
            message_type="block_proposal",
            message_data={
                "block_id": getattr(block_data, 'id', 'unknown'),
                "height": getattr(block_data, 'height', 0),
                "tx_count": len(getattr(block_data, 'transactions', []))
            }
        )
    
    def log_transaction_broadcast(self, sender, receiver, transaction):
        """Log a transaction broadcast"""
        return self.log_message(
            sender=sender,
            receiver=receiver,
            message_type="transaction",
            message_data={
                "tx_id": getattr(transaction, 'tx_id', 'unknown'),
                "sender": getattr(transaction, 'sender', 'unknown'),
                "receiver": getattr(transaction, 'receiver', 'unknown'),
                "amount": getattr(transaction, 'amount', 0)
            }
        )
    
    def log_sync_request(self, sender, receiver, from_block, to_block):
        """Log a sync request"""
        return self.log_message(
            sender=sender,
            receiver=receiver,
            message_type="sync_request",
            message_data={
                "from_block": from_block,
                "to_block": to_block
            },
            direction="incoming"
        )
    
    def log_error(self, sender, receiver, error_type, error_message):
        """Log a communication error"""
        return self.log_message(
            sender=sender,
            receiver=receiver,
            message_type=f"error_{error_type}",
            message_data={"error": error_message},
            direction="incoming"
        )
    
    def search_logs(self, search_term=None, node_id=None, message_type=None, 
                   direction=None, start_time=None, end_time=None, limit=100):
        """Search through communication logs"""
        results = []
        
        with self.lock:
            for entry in reversed(self.comm_log):
                # Apply filters
                if search_term and search_term.lower() not in str(entry).lower():
                    continue
                if node_id and node_id not in [entry["sender"], entry["receiver"]]:
                    continue
                if message_type and entry["type"] != message_type:
                    continue
                if direction and entry["direction"] != direction:
                    continue
                if start_time and entry["timestamp"] < start_time:
                    continue
                if end_time and entry["timestamp"] > end_time:
                    continue
                
                results.append(entry)
                if len(results) >= limit:
                    break
        
        return results
    
    def get_statistics(self, hours=24):
        """Get communication statistics"""
        cutoff = datetime.now().timestamp() - (hours * 3600)
        cutoff_iso = datetime.fromtimestamp(cutoff).isoformat()
        
        with self.lock:
            recent_logs = [entry for entry in self.comm_log 
                          if entry["timestamp"] > cutoff_iso]
            
            if not recent_logs:
                return {
                    "total_messages": 0,
                    "period_hours": hours,
                    "nodes_communicating": 0
                }
            
            # Count by type
            type_counts = {}
            for entry in recent_logs:
                type_counts[entry["type"]] = type_counts.get(entry["type"], 0) + 1
            
            # Count by direction
            outgoing = sum(1 for entry in recent_logs if entry["direction"] == "outgoing")
            incoming = len(recent_logs) - outgoing
            
            # Get unique nodes
            all_nodes = set()
            for entry in recent_logs:
                all_nodes.add(entry["sender"])
                all_nodes.add(entry["receiver"])
            
            # Calculate message rate
            if len(recent_logs) > 1:
                first_time = datetime.fromisoformat(recent_logs[0]["timestamp"])
                last_time = datetime.fromisoformat(recent_logs[-1]["timestamp"])
                time_diff = (last_time - first_time).total_seconds()
                if time_diff > 0:
                    messages_per_hour = len(recent_logs) / (time_diff / 3600)
                else:
                    messages_per_hour = 0
            else:
                messages_per_hour = 0
            
            return {
                "total_messages": len(recent_logs),
                "period_hours": hours,
                "outgoing_messages": outgoing,
                "incoming_messages": incoming,
                "unique_nodes": len(all_nodes),
                "messages_per_hour": round(messages_per_hour, 1),
                "message_types": type_counts,
                "data_volume_mb": round(sum(entry["data_size"] for entry in recent_logs) / (1024 * 1024), 2)
            }
    
    def export_logs(self, filename=None, format="json", limit=1000):
        """Export logs to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"comm_log_export_{timestamp}.{format}"
        
        with self.lock:
            logs_to_export = list(self.comm_log)[-limit:]  # Last N entries
        
        try:
            if format == "json":
                with open(filename, 'w') as f:
                    json.dump(logs_to_export, f, indent=2)
            elif format == "csv":
                import csv
                with open(filename, 'w', newline='') as f:
                    if logs_to_export:
                        writer = csv.DictWriter(f, fieldnames=logs_to_export[0].keys())
                        writer.writeheader()
                        writer.writerows(logs_to_export)
            else:
                print(f"[COMM-LOG] Unsupported format: {format}")
                return False
            
            print(f"[COMM-LOG] Exported {len(logs_to_export)} entries to {filename}")
            return True
            
        except Exception as e:
            print(f"[COMM-LOG] Export error: {e}")
            return False
    
    def clear_logs(self, keep_last=1000):
        """Clear old logs, keeping only the most recent N"""
        with self.lock:
            current_size = len(self.comm_log)
            if current_size <= keep_last:
                return 0
            
            # Keep only last N entries
            self.comm_log = deque(list(self.comm_log)[-keep_last:], maxlen=self.comm_log.maxlen)
            cleared = current_size - len(self.comm_log)
            
            print(f"[COMM-LOG] Cleared {cleared} old log entries")
            return cleared
    
    def print_summary(self):
        """Print summary of communication logs"""
        stats = self.get_statistics(hours=1)  # Last hour
        
        print("\n=== NODE COMMUNICATION LOG ===")
        print(f"Total messages (all time): {self.message_count}")
        print(f"Current log size: {len(self.comm_log)}")
        
        if stats["total_messages"] > 0:
            print(f"\nLast hour statistics:")
            print(f"  Messages: {stats['total_messages']}")
            print(f"  Outgoing: {stats['outgoing_messages']}")
            print(f"  Incoming: {stats['incoming_messages']}")
            print(f"  Unique nodes: {stats['unique_nodes']}")
            print(f"  Messages/hour: {stats['messages_per_hour']}")
            print(f"  Data volume: {stats['data_volume_mb']} MB")
            
            if stats["message_types"]:
                print(f"\n  Message types:")
                for msg_type, count in stats["message_types"].items():
                    print(f"    {msg_type}: {count}")
        
        # Show recent messages
        if self.comm_log:
            print(f"\nRecent messages (last 5):")
            for entry in list(self.comm_log)[-5:]:
                time_str = datetime.fromisoformat(entry["timestamp"]).strftime("%H:%M:%S")
                print(f"  [{time_str}] {entry['direction']} {entry['sender']} -> {entry['receiver']}: {entry['type']}")

# Test function
def test_communication_log():
    print("\nTesting NodeCommunicationLog...")
    
    # Create log system
    comm_log = NodeCommunicationLog("test_comm.log", max_entries=100)
    
    # Log some messages
    print("\n1. Logging messages...")
    
    # Block proposal
    class MockBlock:
        def __init__(self):
            self.id = "block_001"
            self.height = 100
            self.transactions = ["tx1", "tx2", "tx3"]
    
    block = MockBlock()
    comm_log.log_block_proposal("node_001", "node_002", block)
    
    # Transaction broadcast
    class MockTx:
        def __init__(self):
            self.tx_id = "tx_001"
            self.sender = "alice"
            self.receiver = "bob"
            self.amount = 100
    
    tx = MockTx()
    comm_log.log_transaction_broadcast("node_001", "node_003", tx)
    
    # Sync request
    comm_log.log_sync_request("node_002", "node_001", 90, 100)
    
    # Error
    comm_log.log_error("node_003", "node_001", "timeout", "Connection timeout")
    
    # Add more messages
    for i in range(10):
        comm_log.log_message(
            sender=f"node_{i%3+1}",
            receiver=f"node_{(i+1)%3+1}",
            message_type="ping",
            message_data={"seq": i, "time": datetime.now().isoformat()},
            direction="outgoing" if i % 2 == 0 else "incoming"
        )
    
    # Get statistics
    print("\n2. Communication statistics...")
    stats = comm_log.get_statistics(hours=24)
    for key, value in stats.items():
        if key != "message_types":
            print(f"{key}: {value}")
    
    # Search logs
    print("\n3. Searching logs...")
    results = comm_log.search_logs(message_type="ping", limit=3)
    print(f"Found {len(results)} ping messages")
    
    # Print summary
    print("\n4. Log summary...")
    comm_log.print_summary()
    
    # Export logs
    print("\n5. Exporting logs...")
    comm_log.export_logs("test_export.json", limit=5)
    
    print("\n✅ Communication log test completed!")

if __name__ == "__main__":
    test_communication_log()
