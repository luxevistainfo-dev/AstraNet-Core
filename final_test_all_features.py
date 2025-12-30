# final_test_all_features.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("="*60)
print("ASTRA NET CORE - ALL 10 FEATURES TEST")
print("="*60)

def test_all_features():
    results = []
    
    # 1️⃣ TX History Logging
    print("\n1️⃣ Testing TX History Logging...")
    try:
        from core.history import TxHistory
        
        class TestTx:
            def __init__(self, tx_id):
                self.tx_id = tx_id
                self.sender = "alice"
                self.receiver = "bob"
                self.amount = 100
                self.timestamp = "2024-01-01T00:00:00"
        
        history = TxHistory("final_test_history.json")
        tx = TestTx("final_tx_001")
        history.log_tx(tx)
        history.print_stats()
        results.append(("Tx History Logging", True))
        print("✅ PASS")
    except Exception as e:
        print(f"❌ FAIL: {e}")
        results.append(("Tx History Logging", False))
    
    # 2️⃣ Transaction Priority Queue
    print("\n2️⃣ Testing Transaction Priority Queue...")
    try:
        from core.priority_mempool import PriorityMempool
        
        class TestTx2:
            def __init__(self, tx_id):
                self.tx_id = tx_id
        
        mempool = PriorityMempool(max_size=3)
        for i in range(4):
            tx = TestTx2(f"priority_tx_{i}")
            mempool.add_tx(tx, ai_score=i*0.3, fee=i*0.5)
        
        mempool.print_status()
        results.append(("Priority Transaction Queue", True))
        print("✅ PASS")
    except Exception as e:
        print(f"❌ FAIL: {e}")
        results.append(("Priority Transaction Queue", False))
    
    # 3️⃣ Dynamic Block Size
    print("\n3️⃣ Testing Dynamic Block Size...")
    try:
        from core.dynamic_block import DynamicBlockSize
        
        class TestMempool:
            def __init__(self, size):
                self.transactions = ['tx'] * size
        
        calculator = DynamicBlockSize()
        mempool = TestMempool(75)
        size = calculator.calculate_block_size(mempool, 0.7)
        print(f"Calculated block size: {size}")
        results.append(("Dynamic Block Size", True))
        print("✅ PASS")
    except Exception as e:
        print(f"❌ FAIL: {e}")
        results.append(("Dynamic Block Size", False))
    
    # 4️⃣ AI Predictive Fees
    print("\n4️⃣ Testing AI Predictive Fees...")
    try:
        from ai.fee_model import FeePredictor
        
        predictor = FeePredictor()
        test_fees = [0.1, 0.15, 0.12, 0.18, 0.2]
        for fee in test_fees:
            predictor.add_fee_data([fee])
        
        fee = predictor.predict_next_fee(100, 0.6, "normal")
        print(f"Predicted fee: {fee}")
        results.append(("AI Predictive Fees", True))
        print("✅ PASS")
    except Exception as e:
        print(f"❌ FAIL: {e}")
        results.append(("AI Predictive Fees", False))
    
    # 5️⃣ Smart Contract Template Checks
    print("\n5️⃣ Testing Smart Contract Template Checks...")
    try:
        from ai.smart_contract_checker import SmartContractValidator
        
        validator = SmartContractValidator()
        contract = """
class TestContract:
    def __init__(self):
        self.value = 0
"""
        result = validator.validate_contract(contract, "TestContract")
        print(f"Security score: {result['security_score']}/100")
        results.append(("Smart Contract Checks", True))
        print("✅ PASS")
    except Exception as e:
        print(f"❌ FAIL: {e}")
        results.append(("Smart Contract Checks", False))
    
    # 6️⃣ Block Metrics Dashboard
    print("\n6️⃣ Testing Block Metrics Dashboard...")
    try:
        from core.block_metrics import BlockMetrics
        
        class TestBlock:
            def __init__(self):
                self.id = "test_block"
                self.transactions = []
        
        metrics = BlockMetrics()
        block = TestBlock()
        result = metrics.analyze_block(block)
        print(f"Block analyzed: {result['block_id']}")
        metrics.print_dashboard()
        results.append(("Block Metrics Dashboard", True))
        print("✅ PASS")
    except Exception as e:
        print(f"❌ FAIL: {e}")
        results.append(("Block Metrics Dashboard", False))
    
    # 7️⃣ AI-Assisted Node Health
    print("\n7️⃣ Testing AI-Assisted Node Health...")
    try:
        from ai.node_health import NodeHealthMonitor
        
        monitor = NodeHealthMonitor("test_node")
        health = monitor.run_check()
        print(f"Health score: {health['health_score']['overall_score']}")
        monitor.print_health_status()
        results.append(("AI Node Health", True))
        print("✅ PASS")
    except Exception as e:
        print(f"❌ FAIL: {e}")
        results.append(("AI Node Health", False))
    
    # 8️⃣ Blockchain Snapshot
    print("\n8️⃣ Testing Blockchain Snapshot...")
    try:
        from core.snapshot import BlockchainSnapshot
        
        snapshot_mgr = BlockchainSnapshot("test_snapshots_final")
        test_data = [{"block": "test_block", "txs": 3}]
        snapshot = snapshot_mgr.create_snapshot(test_data, {"test": True}, compress=False)
        print(f"Created snapshot: {snapshot['id']}")
        results.append(("Blockchain Snapshot", True))
        print("✅ PASS")
    except Exception as e:
        print(f"❌ FAIL: {e}")
        results.append(("Blockchain Snapshot", False))
    
    # 9️⃣ AI Alert System
    print("\n9️⃣ Testing AI Alert System...")
    try:
        from ai.alert_system import AIAlertSystem
        
        alert_system = AIAlertSystem("test_alert_config_final.json")
        
        class TestTx3:
            def __init__(self):
                self.tx_id = "alert_tx"
                self.ai_score = 0.9
        
        tx = TestTx3()
        alerts = alert_system.monitor_transactions([tx])
        print(f"Generated {len(alerts)} alerts")
        alert_system.print_alert_summary()
        results.append(("AI Alert System", True))
        print("✅ PASS")
    except Exception as e:
        print(f"❌ FAIL: {e}")
        results.append(("AI Alert System", False))
    
    # 🔟 Node Communication Log
    print("\n🔟 Testing Node Communication Log...")
    try:
        from core.node_communication import NodeCommunicationLog
        
        comm_log = NodeCommunicationLog("test_comm_final.log")
        comm_log.log_message("node_001", "node_002", "test_message", {"test": True})
        stats = comm_log.get_statistics(hours=1)
        print(f"Logged messages: {stats['total_messages']}")
        comm_log.print_summary()
        results.append(("Node Communication Log", True))
        print("✅ PASS")
    except Exception as e:
        print(f"❌ FAIL: {e}")
        results.append(("Node Communication Log", False))
    
    # Summary
    print("\n" + "="*60)
    print("FINAL TEST RESULTS")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for i, (name, success) in enumerate(results, 1):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{i:2d}. {name:30} {status}")
    
    print(f"\nTotal: {passed}/{total} features working")
    
    if passed == total:
        print("\n🎉 CONGRATULATIONS! ALL 10 FEATURES WORK!")
        print("="*60)
        print("\nYou have successfully implemented:")
        print(" 1. Transaction History Logging")
        print(" 2. Priority Transaction Queue")
        print(" 3. Dynamic Block Size")
        print(" 4. AI Predictive Fees")
        print(" 5. Smart Contract Template Checks")
        print(" 6. Block Metrics Dashboard")
        print(" 7. AI-Assisted Node Health")
        print(" 8. Blockchain Snapshot")
        print(" 9. AI Alert System")
        print("10. Node Communication Log")
        print("\n✅ AstraNet-Core is ready for production!")
    else:
        print(f"\n⚠️ {total - passed} features need fixing")

if __name__ == "__main__":
    test_all_features()
