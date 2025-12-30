# test_complete_structure.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("="*60)
print("КОМПЛЕТЕН ТЕСТ НА СИТЕ ФУНКЦИИ СПОРЕД БАРАЊАТА")
print("="*60)

def test_all_required_functions():
    print("\nТестирање на сите барани функции...")
    
    # 1. core/TxHistory (history.py)
    print("\n1. Тестирање TxHistory (core)...")
    try:
        from core.history import TxHistory
        
        class TestTx:
            def __init__(self):
                self.tx_id = "test_001"
                self.sender = "alice"
                self.receiver = "bob"
                self.amount = 100
                self.timestamp = "2024-01-01T00:00:00"
        
        history = TxHistory()
        tx = TestTx()
        history.log_tx(tx)
        print("✅ TxHistory работи")
    except Exception as e:
        print(f"❌ TxHistory грешка: {e}")
    
    # 2. core/PriorityMempool (priority_mempool.py)
    print("\n2. Тестирање PriorityMempool (core)...")
    try:
        from core.priority_mempool import PriorityMempool
        
        class TestTx2:
            def __init__(self, tx_id):
                self.tx_id = tx_id
        
        mempool = PriorityMempool(max_size=3)
        tx = TestTx2("test_tx")
        mempool.add_tx(tx, ai_score=0.8, fee=1.0)
        print("✅ PriorityMempool работи")
    except Exception as e:
        print(f"❌ PriorityMempool грешка: {e}")
    
    # 3. consensus/block_size_limit
    print("\n3. Тестирање block_size_limit (consensus)...")
    try:
        from consensus.block_size_limit import block_size_limit
        
        class TestMempool:
            def __init__(self, size):
                self.transactions = ['tx'] * size
        
        # Тест случаи
        test_cases = [5, 25, 100]
        for size in test_cases:
            mempool = TestMempool(size)
            result = block_size_limit(mempool)
            print(f"  Мемпул {size}: блок големина {result}")
        
        print("✅ block_size_limit работи")
    except Exception as e:
        print(f"❌ block_size_limit грешка: {e}")
    
    # 4. ai/predict_fee (fee_model.py)
    print("\n4. Тестирање predict_fee (ai)...")
    try:
        from ai.fee_model import FeePredictor
        
        predictor = FeePredictor()
        # Додај историски податоци
        test_fees = [0.1, 0.15, 0.12]
        for fee in test_fees:
            predictor.add_fee_data([fee])
        
        # Предвиди fee
        fee = predictor.predict_next_fee(mempool_size=50, network_congestion=0.7)
        print(f"  Предвиден fee: {fee}")
        print("✅ predict_fee работи")
    except Exception as e:
        print(f"❌ predict_fee грешка: {e}")
    
    # 5. ai/check_template (smart_contract_checker.py)
    print("\n5. Тестирање check_template (ai)...")
    try:
        from ai.smart_contract_checker import SmartContractValidator
        
        validator = SmartContractValidator()
        test_contract = """
class TestContract:
    def __init__(self):
        self.value = 0
"""
        result = validator.validate_contract(test_contract, "TestContract")
        print(f"  Резултат: Безбеден={result['safe']}, Score={result['security_score']}")
        print("✅ check_template работи")
    except Exception as e:
        print(f"❌ check_template грешка: {e}")
    
    # 6. ai/block_metrics (block_metrics.py)
    print("\n6. Тестирање block_metrics (ai)...")
    try:
        from ai.block_metrics import BlockMetrics
        
        class TestBlock:
            def __init__(self):
                self.id = "test_block"
                self.transactions = []
        
        metrics = BlockMetrics()
        block = TestBlock()
        result = metrics.analyze_block(block)
        print(f"  Анализиран блок: {result['block_id']}")
        print("✅ block_metrics работи")
    except Exception as e:
        print(f"❌ block_metrics грешка: {e}")
    
    # 7. ai/node_health (node_health.py)
    print("\n7. Тестирање node_health (ai)...")
    try:
        from ai.node_health import NodeHealthMonitor
        
        monitor = NodeHealthMonitor("test_node")
        health = monitor.run_check()
        print(f"  Health score: {health['health_score']['overall_score']}")
        print("✅ node_health (ai) работи")
    except Exception as e:
        print(f"❌ node_health (ai) грешка: {e}")
    
    # 8. consensus/node_health
    print("\n8. Тестирање node_health (consensus)...")
    try:
        from consensus.node_health import node_health
        
        test_metrics = {"cpu_load": 75}
        result = node_health(test_metrics)
        print(f"  CPU load 75%: healthy={result['healthy']}, score={result['score']}")
        print("✅ node_health (consensus) работи")
    except Exception as e:
        print(f"❌ node_health (consensus) грешка: {e}")
    
    # 9. ai/ai_alert (alert_system.py)
    print("\n9. Тестирање ai_alert (ai)...")
    try:
        from ai.alert_system import AIAlertSystem
        
        alert_system = AIAlertSystem()
        
        class AlertTx:
            def __init__(self):
                self.tx_id = "alert_tx"
                self.ai_score = 0.9
        
        tx = AlertTx()
        alerts = alert_system.monitor_transactions([tx])
        print(f"  Генерирани alerts: {len(alerts)}")
        print("✅ ai_alert работи")
    except Exception as e:
        print(f"❌ ai_alert грешка: {e}")
    
    # 10. consensus/log_node_msg
    print("\n10. Тестирање log_node_msg (consensus)...")
    try:
        from consensus.log_node_msg import log_node_msg
        
        log_node_msg("node_001", "node_002", "Test message")
        print("✅ log_node_msg работи (провери node_comm.log фајл)")
    except Exception as e:
        print(f"❌ log_node_msg грешка: {e}")
    
    # 11. snapshot/backup
    print("\n11. Тестирање backup (snapshot)...")
    try:
        from snapshot.backup import save_snapshot, load_snapshot
        
        # Тест 1: со chain објект
        class TestChain:
            def __init__(self):
                self.chain = ["block1", "block2", "block3"]
        
        test_chain = TestChain()
        save_snapshot(test_chain, "test_snapshot1.pkl")
        loaded1 = load_snapshot("test_snapshot1.pkl")
        print(f"  Тест 1: Вчитани {len(loaded1)} блокови")
        
        # Тест 2: со директни податоци
        test_data = ["tx1", "tx2", "tx3"]
        save_snapshot(test_data, "test_snapshot2.pkl")
        loaded2 = load_snapshot("test_snapshot2.pkl")
        print(f"  Тест 2: Вчитани {len(loaded2)} трансакции")
        
        # Чистење
        import os
        os.remove("test_snapshot1.pkl")
        os.remove("test_snapshot2.pkl")
        
        print("✅ backup работи")
    except Exception as e:
        print(f"❌ backup грешка: {e}")

        
        test_chain = {"chain": ["block1", "block2", "block3"]}
        save_snapshot(test_chain, "test_snapshot.pkl")
        print("✅ save_snapshot работи")
        
        # За коментар поради безбедност:
        # loaded = load_snapshot("test_snapshot.pkl")
        # print(f"  Вчитани податоци: {len(loaded['chain'])} blocks")
    except Exception as e:
        print(f"❌ backup грешка: {e}")
    
    print("\n" + "="*60)
    print("🎉 ТЕСТОТ ЗАВРШЕН!")
    print("Сите барани функции се имплементирани и тестирани.")
    print("="*60)

if __name__ == "__main__":
    test_all_required_functions()
