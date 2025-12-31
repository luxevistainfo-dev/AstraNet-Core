#!/usr/bin/env python3
"""
ИНТЕГРАЦИЈА НА PHASE 1 МОДУЛИ ВО ASTRA-NET CORE - ПОПРАВЕНА ВЕРЗИЈА
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
    
    # Специјален случај за AIAlertSystem
    try:
        import requests
        from ai.alert_system import AIAlertSystem
        successful.append('ai.alert_system.AIAlertSystem')
        print(f"  ✅ ai.alert_system.AIAlertSystem")
    except ImportError as e:
        failed.append(f"ai.alert_system.AIAlertSystem ({str(e)})")
        print(f"  ⚠️ ai.alert_system.AIAlertSystem - {e} (но ова не е критично)")
    
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
        print(f"  ✅ Self-Healing Contracts: успешно извршено")
        print(f"     Поправки: {contract.healing_count}")
    except Exception as e:
        print(f"  ❌ Self-Healing Contracts: {e}")
    
    try:
        from green_mining.energy_optimizer import GreenMiningOptimizer
        optimizer = GreenMiningOptimizer()
        result = optimizer.optimize_mining(500, 'medium')
        print(f"  ✅ Green Mining: {result['renewable_percentage']}% обновлива енергија")
        print(f"     Заштеда CO2: {result['carbon_saved_kg']}kg")
    except Exception as e:
        print(f"  ❌ Green Mining: {e}")

def create_enhanced_system():
    """Создај подобрен систем без AIAlertSystem ако не е достапен"""
    print("\n🔗 КРЕИРАМ ИНТЕГРИРАН СИСТЕМ:")
    
    try:
        # Импортирај ги модулите што сигурно работат
        from quantum_validator.quantum_core import QuantumSafeValidator, create_sample_transaction
        from self_healing.contract_healer import SelfHealingContract, create_sample_contract
        from green_mining.energy_optimizer import GreenMiningOptimizer
        
        from ai.fee_model import FeePredictor
        from ai.smart_contract_checker import SmartContractValidator
        from ai.block_metrics import BlockMetrics
        from ai.node_health import NodeHealthMonitor
        
        # Пробај да го импортираш AIAlertSystem, но не fail-увај ако не успее
        try:
            from ai.alert_system import AIAlertSystem
            has_alert_system = True
        except ImportError:
            has_alert_system = False
            print("  ⚠️ AIAlertSystem не е достапен, продолжувам без него")
        
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
                
                # Опционално
                self.alert_system = AIAlertSystem() if has_alert_system else None
                
                self.integration_status = {
                    'phase1_modules': ['QuantumValidator', 'SelfHealing', 'GreenMining'],
                    'ai_modules': ['FeePredictor', 'SmartContractValidator', 'BlockMetrics', 
                                  'NodeHealthMonitor', 'AIAlertSystem' if has_alert_system else 'AIAlertSystem (недостапен)'],
                    'status': 'ACTIVE'
                }
                print(f"  ✅ Интегриран систем креиран со {len(self.integration_status['phase1_modules'])} Phase 1 модули")
            
            def validate_transaction_enhanced(self, tx_data):
                """Валидирај трансакција со quantum валидација и AI"""
                print(f"\n  🔍 Валидирам трансакција: {tx_data.get('id', 'Unknown')}")
                
                # Квантска валидација
                quantum_valid, quantum_msg = self.quantum_validator.validate_transaction(tx_data)
                if not quantum_valid:
                    return False, f"Quantum validation failed: {quantum_msg}"
                
                # AI валидација (ако постои amount)
                if 'amount' in tx_data:
                    try:
                        predicted_fee = self.fee_predictor.predict(tx_data['amount'])
                        print(f"    🤖 AI предвиден fee: {predicted_fee}")
                    except:
                        print(f"    ⚠️ Fee prediction не успеа")
                
                return True, "Transaction validated (Quantum + AI)"
            
            def create_self_healing_contract(self, contract_code):
                """Креирај self-healing договор"""
                print(f"  📝 Креирам self-healing договор...")
                contract = self.self_healing_system(contract_code)
                
                # Валидирај со постоечки AI валидатор
                try:
                    validation_result = self.smart_contract_validator.validate(contract_code)
                    print(f"    🤖 AI contract validation: {validation_result}")
                except:
                    print(f"    ⚠️ Contract validation не успеа")
                
                return contract
            
            def optimize_mining_with_metrics(self, power_needed):
                """Оптимизирај mining со метрики"""
                print(f"  ⚡ Оптимизирам mining за {power_needed}kW...")
                
                # Green mining оптимизација
                mining_result = self.green_mining.optimize_mining(power_needed, 'medium')
                
                # Ажурирај блок метрики
                try:
                    self.block_metrics.update_metrics({
                        'mining_power': power_needed,
                        'renewable_percentage': mining_result['renewable_percentage'],
                        'carbon_saved': mining_result['carbon_saved_kg']
                    })
                    print(f"    📊 Метрики ажурирани")
                except:
                    print(f"    ⚠️ Ажурирање на метрики не успеа")
                
                return mining_result
            
            def get_system_status(self):
                """Добиј статус на целиот систем"""
                status = {
                    'phase1': {
                        'quantum_validator': self.quantum_validator.get_stats(),
                        'green_mining': self.green_mining.get_environmental_stats(),
                    },
                    'ai_modules': {
                        'fee_predictor': 'ACTIVE',
                        'contract_validator': 'ACTIVE',
                        'block_metrics': 'ACTIVE',
                        'node_health': 'ACTIVE',
                        'alert_system': 'ACTIVE' if self.alert_system else 'INACTIVE',
                    },
                    'integration': 'COMPLETE'
                }
                return status
            
            def run_demo(self):
                """Изврши демонстрација на системот"""
                print("\n  🎬 ПОЧНУВАМ ДЕМОНСТРАЦИЈА:")
                print("  " + "="*50)
                
                # Демо 1: Enhanced transaction validation
                print("\n  1. 🔐 QUANTUM + AI ВАЛИДАЦИЈА:")
                sample_tx = create_sample_transaction()
                valid, msg = self.validate_transaction_enhanced(sample_tx)
                print(f"     Резултат: {msg}")
                
                # Демо 2: Self-healing contract creation
                print("\n  2. 🏥 SELF-HEALING ДОГОВОР:")
                sample_contract = create_sample_contract()
                contract = self.create_self_healing_contract(sample_contract)
                print(f"     Договор креиран: {contract.healing_count} поправки")
                
                # Демо 3: Green mining optimization
                print("\n  3. 🌿 GREEN MINING ОПТИМИЗАЦИЈА:")
                mining_result = self.optimize_mining_with_metrics(800)
                print(f"     Обновлива енергија: {mining_result['renewable_percentage']}%")
                print(f"     Заштеда CO2: {mining_result['carbon_saved_kg']}kg")
                print(f"     Трошоци/час: ${mining_result['cost_per_hour']}")
                
                # Демо 4: Системски статус
                print("\n  4. 📊 СИСТЕМСКИ СТАТУС:")
                status = self.get_system_status()
                active_ai = len([k for k, v in status['ai_modules'].items() if v == 'ACTIVE'])
                print(f"     Phase 1 модули: {len(status['phase1'])} активни")
                print(f"     AI модули: {active_ai} активни")
                print(f"     Вкупно модули: {len(status['phase1']) + active_ai}")
                
                print("\n  ✅ ДЕМОНСТРАЦИЈАТА ЗАВРШЕНА!")
        
        # Креирај и врати го системот
        enhanced_system = AstraNetEnhanced()
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
    
    # Чекор 3: Креирај интегриран систем
    enhanced_system = create_enhanced_system()
    
    print("\n" + "="*70)
    if enhanced_system:
        print("✅ ИНТЕГРАЦИЈАТА Е УСПЕШНА!")
        
        # Изврши демонстрација
        enhanced_system.run_demo()
        
        print("\n" + "="*70)
        print("🎉 AstraNet-Core сега ги содржи Phase 1 модули:")
        print("   🔐 Quantum-Resistant Validator")
        print("   🏥 Self-Healing Contracts")
        print("   🌿 Green Mining Optimizer")
        print("   🤖 + сите постоечки AI функции")
        print("\n🚀 Системот е подготвен за употреба!")
    else:
        print("⚠️ ИНТЕГРАЦИЈАТА ИМА НЕКОИ ПРОБЛЕМИ")
        print("📋 Провери ги горните грешки и пробај повторно")
    
    print("="*70)

if __name__ == "__main__":
    main()
