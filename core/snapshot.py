# core/snapshot.py

import pickle
import json
import gzip
import os
from datetime import datetime
import hashlib

class BlockchainSnapshot:
    def __init__(self, snapshot_dir="snapshots"):
        self.snapshot_dir = snapshot_dir
        os.makedirs(snapshot_dir, exist_ok=True)
        print(f"[SNAPSHOT] Snapshot directory: {snapshot_dir}")
    
    def create_snapshot(self, blockchain_data, metadata=None, compress=True):
        """
        Create a snapshot of blockchain data
        
        Args:
            blockchain_data: The blockchain data (list of blocks, state, etc.)
            metadata: Additional metadata about the snapshot
            compress: Whether to compress the snapshot
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_id = f"snapshot_{timestamp}"
        
        # Prepare snapshot data
        snapshot = {
            "id": snapshot_id,
            "timestamp": datetime.now().isoformat(),
            "blockchain_data": blockchain_data,
            "metadata": metadata or {},
            "checksum": None
        }
        
        # Calculate checksum
        data_str = str(blockchain_data).encode('utf-8')
        snapshot["checksum"] = hashlib.sha256(data_str).hexdigest()
        
        # Determine filename and save method
        if compress:
            filename = os.path.join(self.snapshot_dir, f"{snapshot_id}.pkl.gz")
            self._save_compressed(snapshot, filename)
        else:
            filename = os.path.join(self.snapshot_dir, f"{snapshot_id}.pkl")
            self._save_uncompressed(snapshot, filename)
        
        # Also save metadata as JSON for quick inspection
        metadata_file = os.path.join(self.snapshot_dir, f"{snapshot_id}_metadata.json")
        with open(metadata_file, 'w') as f:
            json.dump({
                "id": snapshot_id,
                "timestamp": snapshot["timestamp"],
                "checksum": snapshot["checksum"],
                "data_size": len(str(blockchain_data)),
                "metadata": snapshot["metadata"]
            }, f, indent=2)
        
        print(f"[SNAPSHOT] Created snapshot: {filename}")
        print(f"[SNAPSHOT] Checksum: {snapshot['checksum']}")
        
        return snapshot
    
    def _save_compressed(self, data, filename):
        """Save data with compression"""
        with gzip.open(filename, 'wb') as f:
            pickle.dump(data, f)
    
    def _save_uncompressed(self, data, filename):
        """Save data without compression"""
        with open(filename, 'wb') as f:
            pickle.dump(data, f)
    
    def load_snapshot(self, snapshot_id=None, filename=None):
        """
        Load a snapshot from file
        
        Args:
            snapshot_id: ID of the snapshot (e.g., "snapshot_20241230_120000")
            filename: Direct filename to load
        """
        if filename is None:
            if snapshot_id is None:
                # Load the latest snapshot
                snapshots = self.list_snapshots()
                if not snapshots:
                    print("[SNAPSHOT] No snapshots available")
                    return None
                filename = snapshots[-1]["filename"]
            else:
                # Try to find the snapshot file
                possible_files = [
                    os.path.join(self.snapshot_dir, f"{snapshot_id}.pkl"),
                    os.path.join(self.snapshot_dir, f"{snapshot_id}.pkl.gz")
                ]
                
                for file in possible_files:
                    if os.path.exists(file):
                        filename = file
                        break
                else:
                    print(f"[SNAPSHOT] Snapshot {snapshot_id} not found")
                    return None
        
        # Load the snapshot
        try:
            if filename.endswith('.gz'):
                with gzip.open(filename, 'rb') as f:
                    snapshot = pickle.load(f)
            else:
                with open(filename, 'rb') as f:
                    snapshot = pickle.load(f)
            
            # Verify checksum
            if self._verify_checksum(snapshot):
                print(f"[SNAPSHOT] Loaded snapshot: {snapshot['id']}")
                print(f"[SNAPSHOT] Timestamp: {snapshot['timestamp']}")
                return snapshot
            else:
                print("[SNAPSHOT] WARNING: Checksum verification failed!")
                return snapshot
                
        except Exception as e:
            print(f"[SNAPSHOT] Error loading snapshot: {e}")
            return None
    
    def _verify_checksum(self, snapshot):
        """Verify the checksum of loaded snapshot"""
        if "checksum" not in snapshot:
            return True  # No checksum to verify
        
        data_str = str(snapshot["blockchain_data"]).encode('utf-8')
        calculated_checksum = hashlib.sha256(data_str).hexdigest()
        
        return snapshot["checksum"] == calculated_checksum
    
    def list_snapshots(self):
        """List all available snapshots"""
        snapshots = []
        
        for filename in os.listdir(self.snapshot_dir):
            if filename.endswith(('.pkl', '.pkl.gz')):
                filepath = os.path.join(self.snapshot_dir, filename)
                stats = os.stat(filepath)
                
                snapshot_id = filename.split('.')[0]
                if snapshot_id.endswith('_metadata'):
                    continue
                
                snapshots.append({
                    "id": snapshot_id,
                    "filename": filepath,
                    "size_bytes": stats.st_size,
                    "modified": datetime.fromtimestamp(stats.st_mtime).isoformat(),
                    "compressed": filename.endswith('.gz')
                })
        
        # Sort by modification time (oldest first)
        snapshots.sort(key=lambda x: x["modified"])
        
        return snapshots
    
    def delete_snapshot(self, snapshot_id):
        """Delete a snapshot and its metadata"""
        deleted = 0
        
        # Delete main snapshot file (compressed and uncompressed)
        for ext in ['.pkl', '.pkl.gz']:
            filename = os.path.join(self.snapshot_dir, f"{snapshot_id}{ext}")
            if os.path.exists(filename):
                os.remove(filename)
                deleted += 1
                print(f"[SNAPSHOT] Deleted: {filename}")
        
        # Delete metadata file
        metadata_file = os.path.join(self.snapshot_dir, f"{snapshot_id}_metadata.json")
        if os.path.exists(metadata_file):
            os.remove(metadata_file)
            deleted += 1
        
        if deleted > 0:
            print(f"[SNAPSHOT] Deleted {deleted} files for snapshot {snapshot_id}")
        else:
            print(f"[SNAPSHOT] No files found for snapshot {snapshot_id}")
        
        return deleted > 0
    
    def cleanup_old_snapshots(self, keep_last=5):
        """Clean up old snapshots, keeping only the N most recent"""
        snapshots = self.list_snapshots()
        
        if len(snapshots) <= keep_last:
            print(f"[SNAPSHOT] No cleanup needed. Have {len(snapshots)}, keeping {keep_last}")
            return 0
        
        to_delete = snapshots[:-keep_last]  # All except last N
        deleted_count = 0
        
        for snapshot in to_delete:
            if self.delete_snapshot(snapshot["id"]):
                deleted_count += 1
        
        print(f"[SNAPSHOT] Cleanup: Deleted {deleted_count} old snapshots")
        return deleted_count
    
    def get_snapshot_stats(self):
        """Get statistics about snapshots"""
        snapshots = self.list_snapshots()
        
        if not snapshots:
            return {"total_snapshots": 0, "total_size_bytes": 0}
        
        total_size = sum(s["size_bytes"] for s in snapshots)
        compressed_count = sum(1 for s in snapshots if s["compressed"])
        
        return {
            "total_snapshots": len(snapshots),
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "compressed_snapshots": compressed_count,
            "uncompressed_snapshots": len(snapshots) - compressed_count,
            "oldest_snapshot": snapshots[0]["modified"] if snapshots else None,
            "newest_snapshot": snapshots[-1]["modified"] if snapshots else None
        }
    
    def print_snapshot_info(self):
        """Print information about all snapshots"""
        snapshots = self.list_snapshots()
        
        print("\n=== BLOCKCHAIN SNAPSHOTS ===")
        
        if not snapshots:
            print("No snapshots available")
            return
        
        stats = self.get_snapshot_stats()
        print(f"Total snapshots: {stats['total_snapshots']}")
        print(f"Total size: {stats['total_size_mb']} MB")
        print(f"Compressed: {stats['compressed_snapshots']}")
        print(f"Uncompressed: {stats['uncompressed_snapshots']}")
        
        print("\nSnapshot list:")
        for i, snapshot in enumerate(snapshots[-5:], 1):  # Last 5
            size_mb = snapshot["size_bytes"] / (1024 * 1024)
            print(f"{i}. {snapshot['id']}")
            print(f"   Size: {size_mb:.2f} MB, Compressed: {snapshot['compressed']}")
            print(f"   Modified: {snapshot['modified']}")

# Test function
def test_snapshot():
    print("\nTesting BlockchainSnapshot...")
    
    # Create test blockchain data
    test_blockchain = [
        {
            "block_id": "block_001",
            "transactions": ["tx1", "tx2", "tx3"],
            "timestamp": "2024-01-01T00:00:00"
        },
        {
            "block_id": "block_002",
            "transactions": ["tx4", "tx5"],
            "timestamp": "2024-01-01T00:10:00"
        },
        {
            "block_id": "block_003",
            "transactions": ["tx6", "tx7", "tx8", "tx9"],
            "timestamp": "2024-01-01T00:20:00"
        }
    ]
    
    metadata = {
        "chain_id": "testnet_001",
        "version": "1.0.0",
        "description": "Test snapshot"
    }
    
    # Create snapshot manager
    snapshot_mgr = BlockchainSnapshot("test_snapshots")
    
    # Create a snapshot
    print("\n1. Creating snapshot...")
    snapshot = snapshot_mgr.create_snapshot(test_blockchain, metadata, compress=True)
    
    # List snapshots
    print("\n2. Listing snapshots...")
    snapshot_mgr.print_snapshot_info()
    
    # Load snapshot
    print("\n3. Loading snapshot...")
    loaded = snapshot_mgr.load_snapshot(snapshot["id"])
    
    if loaded:
        print(f"Loaded snapshot ID: {loaded['id']}")
        print(f"Block count: {len(loaded['blockchain_data'])}")
    
    # Get statistics
    print("\n4. Snapshot statistics...")
    stats = snapshot_mgr.get_snapshot_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # Cleanup (keep only 1 for testing)
    print("\n5. Cleaning up old snapshots...")
    snapshot_mgr.cleanup_old_snapshots(keep_last=1)
    
    print("\n✅ Snapshot test completed!")

if __name__ == "__main__":
    test_snapshot()
