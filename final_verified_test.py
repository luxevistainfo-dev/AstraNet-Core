# final_verified_test.py
import sys
import os
import json
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("="*60)
print("🚀 КОМПЛЕТЕН ТЕСТ - СИТЕ ФУНКЦИИ ВЕРИФИЦИРАНИ")
print("="*60)

class MockTransaction:
    def __init__(self, tx_id, sender, receiver, amount, fee=0, ai_score=0.5):
        self.tx_id = tx_id
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.fee = fee
        self.timestamp = datetime.now().isoformat()
        self.ai_score = ai_score

def run_verified_tests():
    results = []
    
    print("\n📋 СПИСОК НА СИТЕ ФУНКЦИИ:")
    print("="*60)
    
    # 1. CORE - TxHistory
    print("\n1️⃣ CORE: TxHistory (history.py)")
    try:
        from core.history import TxHistory
        history = TxHistory("verified_test.json")
        tx = MockTransaction("verified_001", "alice", "bob", 100)
        history.log_tx(tx)
        print("   ✅ Имплементирано")
        results.append(("CORE: TxHistory", True))
    except Exception as e:
        print(f"   ❌ Грешка: {e}")
        results.append(("CORE: TxHistory", False))
    
    # 2. CORE - PriorityMempool  
    print("\n2️⃣ CORE: PriorityMempool (priority_mempool.py)")
    try:
        from core.priority_mempool import PriorityMempool
        mempool = PriorityMempool(max_size=3)
        tx = MockTransaction("priority_tx", "alice", "bob", 50)
        mempool.add_tx(tx, ai_score=0.8, fee=1.0)
        print("   ✅ Имплементирано")
        results.append(("CORE: PriorityMempool", True))
    except Exception as e:
        print(f"   ❌ Грешка: {e}")
        results.append(("CORE: PriorityMempool", False))
    
    # 3. CORE - Dynamic Block Size
    print("\n3️⃣ CORE: Dynamic Block Size (dynamic_block.py)")
    try:
        from core.dynamic_block import DynamicBlockSize
        calculator = DynamicBlockSize()
        class MockMempool:
            def __init__(self): self.transactions = ['tx'] * 75
        size = calculator.calculate_block_size(MockMempool(), 0.6)
        print(f"   ✅ Имплементирано (блок големина: {size})")
        results.append(("CORE: Dynamic Block Size", True))
    except Exception as e:
        print(f"   ❌ Грешка: {e}")
        results.append(("CORE: Dynamic Block Size", False))
    
    # 4. AI - Fee Prediction
    print("\n4️⃣ AI: Fee Prediction (fee_model.py)")
    try:
        from ai.fee_model import FeePredictor
        predictor = FeePredictor()
        predictor.add_fee_data([0.1, 0.15, 0.12])
        fee = predictor.predict_next_fee(100, 0.7, "normal")
        print(f"   ✅ Имплементирано (fee: {fee})")
        results.append(("AI: Fee Prediction", True))
    except Exception as e:
        print(f"   ❌ Грешка: {e}")
        results.append(("AI: Fee Prediction", False))
    
    # 5. AI - Smart Contract Checker
    print("\n5️⃣ AI: Smart Contract Checker (smart_contract_checker.py)")
    try:
        from ai.smart_contract_checker import SmartContractValidator
        validator = SmartContractValidator()
        contract = "class Test: pass"
        result = validator.validate_contract(contract, "Test")
        print(f"   ✅ Имплементирано (score: {result['security_score']})")
        results.append(("AI: Smart Contract Checker", True))
    except Exception as e:
        print(f"   ❌ Грешка: {e}")
        results.append(("AI: Smart Contract Checker", False))
    
    # 6. AI - Block Metrics
    print("\n6️⃣ AI: Block Metrics (block_metrics.py)")
    try:
        from ai.block_metrics import BlockMetrics
        metrics = BlockMetrics()
        class MockBlock:
            def __init__(self): 
                self.id = "test_block"
                self.transactions = []
        block_metrics = metrics.analyze_block(MockBlock())
        print(f"   ✅ Имплементирано (block: {block_metrics['block_id']})")
        results.append(("AI: Block Metrics", True))
    except Exception as e:
        print(f"   ❌ Грешка: {e}")
        results.append(("AI: Block Metrics", False))
    
    # 7. AI - Node Health Monitor
    print("\n7️⃣ AI: Node Health Monitor (node_health.py)")
    try:
        from ai.node_health import NodeHealthMonitor
        monitor = NodeHealthMonitor("test_node")
        health = monitor.run_check()
        print(f"   ✅ Имплементирано (score: {health['health_score']['overall_score']})")
        results.append(("AI: Node Health Monitor", True))
    except Exception as e:
        print(f"   ❌ Грешка: {e}")
        results.append(("AI: Node Health Monitor", False))
    
    # 8. AI - Alert System
    print("\n8️⃣ AI: Alert System (alert_system.py)")
    try:
        from ai.alert_system import AIAlertSystem
        alerts = AIAlertSystem()
        tx = MockTransaction("alert_tx", "a", "b", 100, ai_score=0.9)
        alerts.monitor_transactions([tx])
        print("   ✅ Имплементирано")
        results.append(("AI: Alert System", True))
    except Exception as e:
        print(f"   ❌ Грешка: {e}")
        results.append(("AI: Alert System", False))
    
    # 9. CONSENSUS - Simple Functions
    print("\n9️⃣ CONSENSUS: Три едноставни функции")
    try:
        from consensus.block_size_limit import block_size_limit
        from consensus.node_health import node_health
        from consensus.log_node_msg import log_node_msg
        
        # Test block_size_limit
        class SimpleMempool:
            def __init__(self, size): self.transactions = ['tx'] * size
        
        size1 = block_size_limit(SimpleMempool(5))
        size2 = block_size_limit(SimpleMempool(25))
        size3 = block_size_limit(SimpleMempool(100))
        
        # Test node_health
        health_result = node_health({"cpu_load": 75})
        
        # Test log_node_msg
        log_node_msg("node1", "node2", "test")
        
        print(f"   ✅ Имплементирано (block sizes: {size1},{size2},{size3})")
        results.append(("CONSENSUS: Simple Functions", True))
    except Exception as e:
        print(f"   ❌ Грешка: {e}")
        results.append(("CONSENSUS: Simple Functions", False))
    
    # 10. SNAPSHOT - Backup System
    print("\n🔟 SNAPSHOT: Backup System (backup.py)")
    try:
        from snapshot.backup import save_snapshot, load_snapshot
        import os
        
        # Test со chain објект
        class TestChain:
            def __init__(self): self.chain = ["block1", "block2"]
        
        chain = TestChain()
        save_snapshot(chain, "test_backup.pkl")
        loaded = load_snapshot("test_backup.pkl")
        
        # Чистење
        if os.path.exists("test_backup.pkl"):
            os.remove("test_backup.pkl")
        
        print(f"   ✅ Имплементирано (loaded {len(loaded)} items)")
        results.append(("SNAPSHOT: Backup System", True))
    except Exception as e:
        print(f"   ❌ Грешка: {e}")
        results.append(("SNAPSHOT: Backup System", False))
    
    # 11. CORE - Node Communication
    print("\n1️⃣1️⃣ CORE: Node Communication (node_communication.py)")
    try:
        from core.node_communication import NodeCommunicationLog
        comm = NodeCommunicationLog("test_comm.log")
        comm.log_message("node1", "node2", "test", {"data": "test"})
        print("   ✅ Имплементирано")
        results.append(("CORE: Node Communication", True))
    except Exception as e:
        print(f"   ❌ Грешка: {e}")
        results.append(("CORE: Node Communication", False))
    
    # 12. CORE - Snapshot (Advanced)
    print("\n1️⃣2️⃣ CORE: Advanced Snapshot (snapshot.py)")
    try:
        from core.snapshot import BlockchainSnapshot
        snapshot_mgr = BlockchainSnapshot("test_snapshots")
        test_data = [{"block": "test"}]
        snapshot = snapshot_mgr.create_snapshot(test_data, {"test": True})
        print(f"   ✅ Имплементирано (ID: {snapshot['id'][:10]}...)")
        results.append(("CORE: Advanced Snapshot", True))
    except Exception as e:
        print(f"   ❌ Грешка: {e}")
        results.append(("CORE: Advanced Snapshot", False))
    
    # РЕЗИМЕ
    print("\n" + "="*60)
    print("📊 ФИНАЛЕН РЕЗИМЕ")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\nВкупно тестови: {total}")
    print(f"Успешни: {passed}")
    print(f"Неуспешни: {total - passed}")
    
    if passed == total:
        print("\n🎉 СУПЕР! СИТЕ ФУНКЦИИ РАБОТАТ!")
    else:
        print(f"\n⚠️  {total - passed} функции треба поправка")
    
    print("\nДЕТАЛЕН РЕЗИМЕ:")
    for i, (name, success) in enumerate(results, 1):
        print(f"{i:2d}. {name:30} {'✅' if success else '❌'}")

if __name__ == "__main__":
    run_verified_tests()

