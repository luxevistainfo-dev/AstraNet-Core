# test_integration.py
import sys
import os
import json
from datetime import datetime

# Add path to modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("="*60)
print("ASTRA NET CORE - INTEGRATION TEST")
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

def run_all_tests():
    print("\n🚀 STARTING TESTS...\n")
    
    # Test 1: TxHistory
    print("1️⃣ TESTING TX HISTORY")
    print("-"*40)
    try:
        from core.history import TxHistory
        history = TxHistory("test_history.json")
        
        for i in range(3):
            tx = MockTransaction(
                tx_id=f"tx_{i}",
                sender=f"addr_{i}",
                receiver=f"addr_{i+1}",
                amount=100 * (i+1),
                fee=i * 0.1
            )
            history.log_tx(tx)
        
        history.print_stats()
        print("✅ TxHistory: PASS")
        test1 = True
    except Exception as e:
        print(f"❌ TxHistory: FAIL - {e}")
        test1 = False
    
    # Test 2: PriorityMempool
    print("\n2️⃣ TESTING PRIORITY MEMPOOL")
    print("-"*40)
    try:
        from core.priority_mempool import PriorityMempool
        mempool = PriorityMempool(max_size=3)
        
        for i in range(4):
            tx = MockTransaction(
                tx_id=f"mem_tx_{i}",
                sender=f"sender_{i}",
                receiver=f"receiver_{i}",
                amount=50 * (i+1)
            )
            mempool.add_tx(tx, ai_score=i*0.3, fee=i*0.5)
        
        mempool.print_status()
        print("✅ PriorityMempool: PASS")
        test2 = True
    except Exception as e:
        print(f"❌ PriorityMempool: FAIL - {e}")
        test2 = False
    
    # Test 3: DynamicBlockSize
    print("\n3️⃣ TESTING DYNAMIC BLOCK SIZE")
    print("-"*40)
    try:
        from core.dynamic_block import DynamicBlockSize
        
        class TestMempool:
            def __init__(self, size):
                self.transactions = ['tx'] * size
        
        calculator = DynamicBlockSize()
        
        for size in [5, 50, 150]:
            mempool = TestMempool(size)
            block_size = calculator.calculate_block_size(mempool, 0.6)
            print(f"Mempool {size} -> Block size {block_size}")
        
        print("✅ DynamicBlockSize: PASS")
        test3 = True
    except Exception as e:
        print(f"❌ DynamicBlockSize: FAIL - {e}")
        test3 = False
    
    # Test 4: FeePredictor
    print("\n4️⃣ TESTING FEE PREDICTOR")
    print("-"*40)
    try:
        from ai.fee_model import FeePredictor
        
        predictor = FeePredictor()
        test_fees = [0.1, 0.15, 0.12, 0.18, 0.2]
        for fee in test_fees:
            predictor.add_fee_data([fee])
        
        fee = predictor.predict_next_fee(100, 0.7, "normal")
        print(f"Predicted fee: {fee}")
        
        advice = predictor.get_fee_advice(500, "normal")
        print(f"Fee advice: {advice['recommended_fee']}")
        
        print("✅ FeePredictor: PASS")
        test4 = True
    except Exception as e:
        print(f"❌ FeePredictor: FAIL - {e}")
        test4 = False
    
    # Test 5: SmartContractValidator
    print("\n5️⃣ TESTING SMART CONTRACT VALIDATOR")
    print("-"*40)
    try:
        from ai.smart_contract_checker import SmartContractValidator
        
        validator = SmartContractValidator()
        contract = """
class TestToken:
    def __init__(self):
        self.balances = {}
    
    def mint(self, to, amount):
        self.balances[to] = self.balances.get(to, 0) + amount
"""
        result = validator.validate_contract(contract, "TestToken")
        print(f"Security score: {result['security_score']}/100")
        print("✅ SmartContractValidator: PASS")
        test5 = True
    except Exception as e:
        print(f"❌ SmartContractValidator: FAIL - {e}")
        test5 = False
    
    # Test 6: BlockMetrics
    print("\n6️⃣ TESTING BLOCK METRICS")
    print("-"*40)
    try:
        from core.block_metrics import BlockMetrics
        
        class TestBlock:
            def __init__(self):
                self.id = "block_001"
                self.transactions = []
        
        metrics = BlockMetrics()
        block = TestBlock()
        result = metrics.analyze_block(block)
        print(f"Block analyzed: {result['block_id']}")
        
        metrics.print_dashboard()
        print("✅ BlockMetrics: PASS")
        test6 = True
    except Exception as e:
        print(f"❌ BlockMetrics: FAIL - {e}")
        test6 = False
    
    # Test 7: NodeHealth
    print("\n7️⃣ TESTING NODE HEALTH")
    print("-"*40)
    try:
        from ai.node_health import NodeHealthMonitor
        
        monitor = NodeHealthMonitor("test_node")
        health = monitor.run_check()
        print(f"Health score: {health['health_score']['overall_score']}")
        
        monitor.print_health_status()
        print("✅ NodeHealthMonitor: PASS")
        test7 = True
    except Exception as e:
        print(f"❌ NodeHealthMonitor: FAIL - {e}")
        test7 = False
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    tests = [
        ("TxHistory", test1),
        ("PriorityMempool", test2),
        ("DynamicBlockSize", test3),
        ("FeePredictor", test4),
        ("SmartContractValidator", test5),
        ("BlockMetrics", test6),
        ("NodeHealth", test7)
    ]
    
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    for name, result in tests:
        print(f"{name}: {'✅ PASS' if result else '❌ FAIL'}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("Implemented features:")
        print("1. Transaction History Logging")
        print("2. Priority Transaction Queue")
        print("3. Dynamic Block Size")
        print("4. AI Fee Prediction")
        print("5. Smart Contract Validation")
        print("6. Block Metrics Dashboard")
        print("7. AI-Assisted Node Health")
    else:
        print(f"\n⚠️ {total - passed} tests failed")

if __name__ == "__main__":
    run_all_tests()
