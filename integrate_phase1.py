#!/usr/bin/env python3
"""
ИНТЕГРАЦИЈА НА PHASE 1 МОДУЛИ ВО ASTRA-NET CORE
"""

import sys
import os
import json

# Додади ги патеките
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("="*70)
print("🚀 ASTRA-NET CORE + BLOCKCHAIN PHASE 1 ИНТЕГРАЦИЈА")
print("="*70)

def check_imports():
    """Провери дали може да се импортираат сите модули"""
    print("\n🔍 ПРОВЕРКА НА ИМПОРТИ:")
    
    modules_to_check = [
        ('quantum_validator.quantum_core', 'QuantumSafeValidator'),
        ('quantum_validator.ai_detector', 'QuantumAIDetector'),
        ('self_healing.contract_healer', 'SelfHealingContract'),
        ('green_mining.energy_optimizer', 'GreenMiningOptimizer'),
        ('ai.fee_model', 'FeePredictor'),
        ('ai.smart_contract_checker', 'SmartContractValidator'),
        ('ai.block_metrics', 'BlockMetrics'),
        ('ai.node_health', 'NodeHealthMonitor'),
        ('ai.alert_system', 'AIAlertSystem'),
    ]
    
    successful = []
    failed = []
    
    for module_name, class_name in modules_to_check:
        try:
            module = __import__(module_name, fromlist=[class_name])
            cls = getattr(module, class_name, None)
            if cls:
                successful.append(f"{module_name}.{class_name}")
                print(f"  ✅ {module_name}.{class_name}")
            else:
                failed.append(f"{module_name}.{class_name} (класа не постои)")
                print(f"  ❌ {module_name}.{class_name} - класа не постои")
        except ImportError as e:
            failed.append(f"{module_name}.{class_name} ({str(e)})")
            print(f"  ❌ {module_name}.{class_name} - {e}")
    
    return successful, failed

def test_phase1_modules():
    """Тестирај ги Phase 1 модулите"""
    print("\n🧪 ТЕСТИРАМ PHASE 1 МОДУЛИ:")
    
    try:
        from quantum_validator.quantum_core import QuantumSafeValidator, create_sample_transaction
        validator = QuantumSafeValidator()
        tx = create_sample_transaction()
        valid, msg = validator.validate_transaction(tx)
        print(f"  ✅ Quantum Validator: {msg}")
    except Exception as e:
        print(f"  ❌ Quantum Validator: {e}")
    
    try:
        from self_healing.contract_healer import SelfHealingContract, create_sample_contract
        contract = SelfHealingContract(create_sample_contract())
        result = contract.execute("transfer", "alice", "bob", 100)
        print(f"  ✅ Self-Healing Contracts: {result.get('success', 'N/A')}")
    except Exception as e:
        print(f"  ❌ Self-Healing Contracts: {e}")
    
    try:
        from green_mining.energy_optimizer import GreenMiningOptimizer
        optimizer = GreenMiningOptimizer()
        result = optimizer.optimize_mining(500, 'medium')
        print(f"  ✅ Green Mining: {result['renewable_percentage']}% renewable")
    except Exception as e:
        print(f"  ❌ Green Mining: {e}")

def test_existing_astranet():
    """Тестирај ги постоечките AstraNet функции"""
    print("\n🤖 ТЕСТИРАМ ПОСТОЕЧКИ ASTRA-NET ФУНКЦИИ:")
    
    # Провери ги AI функциите
    try:
        from ai.fee_model import FeePredictor
        fee_predictor = FeePredictor()
        print(f"  ✅ FeePredictor: Најден")
    except Exception as e:
        print(f"  ❌ FeePredictor: {e}")
    
    try:
        from ai.smart_contract_checker import SmartContractValidator
        sc_validator = SmartContractValidator()
        print(f"  ✅ SmartContractValidator: Најден")
    except Exception as e:
        print(f"  ❌ SmartContractValidator: {e}")
    
    try:
        from ai.block_metrics import BlockMetrics
        metrics = BlockMetrics()
        print(f"  ✅ BlockMetrics: Најден")
    except Exception as e:
        print(f"  ❌ BlockMetrics: {e}")
    
    try:
        from ai.node_health import NodeHealthMonitor
        monitor = NodeHealthMonitor()
        print(f"  ✅ NodeHealthMonitor: Најден")
    except Exception as e:
        print(f"  ❌ NodeHealthMonitor: {e}")
    
    try:
        from ai.alert_system import AIAlertSystem
        alert = AIAlertSystem()
        print(f"  ✅ AIAlertSystem: Најден")
    except Exception as e:
        print(f"  ❌ AIAlertSystem: {e}")

def create_integrated_system():
    """Создај интегриран систем"""
    print("\n🔗 КРЕИРАМ ИНТЕГРИРАН СИСТЕМ:")
    
    try:
        # Импортирај ги сите модули
        from quantum_validator.quantum_core import QuantumSafeValidator
        from self_healing.contract_healer import SelfHealingContract, create_sample_contract
        from green_mining.energy_optimizer import GreenMiningOptimizer
        
        from ai.fee_model import FeePredictor
        from ai.smart_contract_checker import SmartContractValidator
        from ai.block_metrics import BlockMetrics
        from ai.node_health import NodeHealthMonitor
        from ai.alert_system import AIAlertSystem
        
        # Креирај интегрирана класа
        class AstraNetEnhanced:
            """Интегриран AstraNet систем со Phase 1 модули"""
            
            def __init__(self):
                print("  ⚡ Иницијализирам интегриран систем...")
                
                # Phase 1 модули
                self.quantum_validator = QuantumSafeValidator()
                self.self_healing_system = SelfHealingContract
                self.green_mining = GreenMiningOptimizer()
                
                # Постоечки AI модули
                self.fee_predictor = FeePredictor()
                self.smart_contract_validator = SmartContractValidator()
                self.block_metrics = BlockMetrics()
                self.node_health_monitor = NodeHealthMonitor()
                self.alert_system = AIAlertSystem()
                
                self.integration_status = {
                    'phase1_modules': ['QuantumValidator', 'SelfHealing', 'GreenMining'],
                    'ai_modules': ['FeePredictor', 'SmartContractValidator', 'BlockMetrics', 
                                  'NodeHealthMonitor', 'AIAlertSystem'],
                    'status': 'ACTIVE'
                }
            
            def validate_transaction_enhanced(self, tx_data):
                """Валидирај трансакција со quantum валидација и AI"""
                print(f"  🔍 Валидирам трансакција: {tx_data.get('id', 'Unknown')}")
                
                # Квантска валидација
                quantum_valid, quantum_msg = self.quantum_validator.validate_transaction(tx_data)
                if not quantum_valid:
                    return False, f"Quantum validation failed: {quantum_msg}"
                
                # AI валидација (ако постои amount)
                if 'amount' in tx_data:
                    predicted_fee = self.fee_predictor.predict(tx_data['amount'])
                    print(f"    AI предвиден fee: {predicted_fee}")
                
                return True, "Transaction validated (Quantum + AI)"
            
            def create_self_healing_contract(self, contract_code):
                """Креирај self-healing договор"""
                contract = self.self_healing_system(contract_code)
                
                # Валидирај со постоечки AI валидатор
                if hasattr(self.smart_contract_validator, 'validate'):
                    validation_result = self.smart_contract_validator.validate(contract_code)
                    print(f"    AI contract validation: {validation_result}")
                
                return contract
            
            def optimize_mining_with_metrics(self, power_needed):
                """Оптимизирај mining со метрики"""
                # Green mining оптимизација
                mining_result = self.green_mining.optimize_mining(power_needed, 'medium')
                
                # Ажурирај блок метрики
                if hasattr(self.block_metrics, 'update_metrics'):
                    self.block_metrics.update_metrics({
                        'mining_power': power_needed,
                        'renewable_percentage': mining_result['renewable_percentage'],
                        'carbon_saved': mining_result['carbon_saved_kg']
                    })
                
                return mining_result
            
            def get_system_status(self):
                """Добиј статус на целиот систем"""
                status = {
                    'phase1': {
                        'quantum_validator': self.quantum_validator.get_stats(),
                        'green_mining': self.green_mining.get_environmental_stats(),
                    },
                    'ai_modules': {
                        'fee_predictor': 'ACTIVE' if self.fee_predictor else 'INACTIVE',
                        'contract_validator': 'ACTIVE' if self.smart_contract_validator else 'INACTIVE',
                        'block_metrics': 'ACTIVE' if self.block_metrics else 'INACTIVE',
                        'node_health': 'ACTIVE' if self.node_health_monitor else 'INACTIVE',
                        'alert_system': 'ACTIVE' if self.alert_system else 'INACTIVE',
                    },
                    'integration': 'COMPLETE'
                }
                return status
        
        # Тестирај го интегрираниот систем
        enhanced_system = AstraNetEnhanced()
        print("  ✅ Интегриран систем креиран")
        
        # Демо
        print("\n  🎬 ИНТЕГРАЦИСКА ДЕМО:")
        
        # Демо 1: Enhanced transaction validation
        from quantum_validator.quantum_core import create_sample_transaction
        sample_tx = create_sample_transaction()
        valid, msg = enhanced_system.validate_transaction_enhanced(sample_tx)
        print(f"    Enhanced validation: {msg}")
        
        # Демо 2: Self-healing contract creation
        from self_healing.contract_healer import create_sample_contract
        sample_contract = create_sample_contract()
        contract = enhanced_system.create_self_healing_contract(sample_contract)
        print(f"    Self-healing contract created: {contract.healing_count} возможни поправки")
        
        # Демо 3: Green mining optimization
        mining_result = enhanced_system.optimize_mining_with_metrics(800)
        print(f"    Mining optimized: {mining_result['renewable_percentage']}% renewable")
        
        # Статус
        status = enhanced_system.get_system_status()
        print(f"\n  📊 СИСТЕМСКИ СТАТУС:")
        print(f"    Phase 1 модули: {len(status['phase1'])} активни")
        print(f"    AI модули: {len([k for k, v in status['ai_modules'].items() if v == 'ACTIVE'])} активни")
        
        return enhanced_system
        
    except Exception as e:
        print(f"  ❌ Грешка при креирање на интегриран систем: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Главна функција"""
    print("\n" + "="*70)
    print("🚀 ПОЧНУВАМ ИНТЕГРАЦИЈА")
    print("="*70)
    
    # Чекор 1: Провери импортови
    successful, failed = check_imports()
    print(f"\n📊 ИМПОРТ РЕЗУЛТАТИ: {len(successful)} успешни, {len(failed)} неуспешни")
    
    # Чекор 2: Тестирај ги Phase 1 модулите
    test_phase1_modules()
    
    # Чекор 3: Тестирај ги постоечките функции
    test_existing_astranet()
    
    # Чекор 4: Креирај интегриран систем
    integrated_system = create_integrated_system()
    
    print("\n" + "="*70)
    if integrated_system:
        print("✅ ИНТЕГРАЦИЈАТА Е УСПЕШНА!")
        print("🎉 AstraNet-Core сега ги содржи Phase 1 модули:")
        print("   🔐 Quantum-Resistant Validator")
        print("   🏥 Self-Healing Contracts")
        print("   🌿 Green Mining Optimizer")
        print("   🤖 + сите постоечки AI функции")
    else:
        print("⚠️ ИНТЕГРАЦИЈАТА ИМА НЕКОИ ПРОБЛЕМИ")
        print("📋 Провери ги горните грешки и пробај повторно")
    
    print("="*70)

if __name__ == "__main__":
    main()
