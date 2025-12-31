#!/usr/bin/env python3
"""
ASTRA-NET ENHANCED - Главен интегриран систем со Phase 1 модули
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class AstraNetEnhanced:
    """
    Главен интегриран систем на AstraNet-Core со Phase 1 модули
    Ова е фајлот што треба да го користиш во твојот постоечки код
    """
    
    def __init__(self, enable_quantum=True, enable_self_healing=True, enable_green_mining=True):
        """Иницијализирај го интегрираниот систем"""
        print("🚀 Иницијализирам AstraNet Enhanced систем...")
        
        self.modules = {}
        self.enabled_features = {
            'quantum': enable_quantum,
            'self_healing': enable_self_healing,
            'green_mining': enable_green_mining
        }
        
        # Иницијализирај ги модулите
        self._initialize_modules()
        
        print(f"✅ AstraNet Enhanced креиран со {len(self.modules)} активни модули")
    
    def _initialize_modules(self):
        """Иницијализирај ги сите модули"""
        
        # 1. Phase 1 модули
        if self.enabled_features['quantum']:
            try:
                from quantum_validator.quantum_core import QuantumSafeValidator
                self.modules['quantum_validator'] = QuantumSafeValidator()
                print("  ✅ Quantum Validator - АКТИВЕН")
            except Exception as e:
                print(f"  ❌ Quantum Validator - ГРЕШКА: {e}")
        
        if self.enabled_features['self_healing']:
            try:
                from self_healing.contract_healer import SelfHealingContract
                self.modules['self_healing_class'] = SelfHealingContract
                print("  ✅ Self-Healing Contracts - АКТИВЕН")
            except Exception as e:
                print(f"  ❌ Self-Healing Contracts - ГРЕШКА: {e}")
        
        if self.enabled_features['green_mining']:
            try:
                from green_mining.energy_optimizer import GreenMiningOptimizer
                self.modules['green_mining'] = GreenMiningOptimizer()
                print("  ✅ Green Mining Optimizer - АКТИВЕН")
            except Exception as e:
                print(f"  ❌ Green Mining Optimizer - ГРЕШКА: {e}")
        
        # 2. Постоечки AI модули од AstraNet-Core
        try:
            from ai.fee_model import FeePredictor
            self.modules['fee_predictor'] = FeePredictor()
            print("  ✅ Fee Predictor - АКТИВЕН")
        except Exception as e:
            print(f"  ⚠️ Fee Predictor - НЕДОСТАПЕН: {e}")
        
        try:
            from ai.smart_contract_checker import SmartContractValidator
            self.modules['contract_validator'] = SmartContractValidator()
            print("  ✅ Smart Contract Validator - АКТИВЕН")
        except Exception as e:
            print(f"  ⚠️ Smart Contract Validator - НЕДОСТАПЕН: {e}")
        
        try:
            from ai.block_metrics import BlockMetrics
            self.modules['block_metrics'] = BlockMetrics()
            print("  ✅ Block Metrics - АКТИВЕН")
        except Exception as e:
            print(f"  ⚠️ Block Metrics - НЕДОСТАПЕН: {e}")
        
        try:
            from ai.node_health import NodeHealthMonitor
            self.modules['node_health'] = NodeHealthMonitor()
            print("  ✅ Node Health Monitor - АКТИВЕН")
        except Exception as e:
            print(f"  ⚠️ Node Health Monitor - НЕДОСТАПЕН: {e}")
    
    def validate_transaction(self, tx_data, use_quantum=True, use_ai=True):
        """Валидирај трансакција со сите достапни методи"""
        print(f"\n🔍 Валидација на трансакција: {tx_data.get('id', 'Unknown')}")
        
        # Квантска валидација
        if use_quantum and 'quantum_validator' in self.modules:
            is_valid, message = self.modules['quantum_validator'].validate_transaction(tx_data)
            if not is_valid:
                return False, f"Quantum validation failed: {message}"
            print("  ✅ Quantum validation passed")
        
        # AI валидација
        if use_ai and 'fee_predictor' in self.modules and 'amount' in tx_data:
            try:
                fee = self.modules['fee_predictor'].predict(tx_data['amount'])
                print(f"  🤖 AI predicted fee: {fee}")
            except:
                print("  ⚠️ AI fee prediction skipped")
        
        return True, "Transaction validated successfully"
    
    def create_smart_contract(self, contract_code, make_self_healing=True):
        """Креирај паметен договор (може да биде self-healing)"""
        print(f"\n📝 Креирам паметен договор...")
        
        if make_self_healing and 'self_healing_class' in self.modules:
            contract = self.modules['self_healing_class'](contract_code)
            print("  ✅ Self-healing contract created")
            
            # AI валидација
            if 'contract_validator' in self.modules:
                try:
                    result = self.modules['contract_validator'].validate(contract_code)
                    print(f"  🤖 AI contract validation: {result}")
                except:
                    print("  ⚠️ AI contract validation skipped")
        else:
            # Основен договор
            contract = {'code': contract_code, 'type': 'basic'}
            print("  ✅ Basic contract created")
        
        return contract
    
    def optimize_mining_operation(self, power_needed_kw, urgency='medium'):
        """Оптимизирај mining операција"""
        print(f"\n⚡ Оптимизација на mining за {power_needed_kw}kW...")
        
        if 'green_mining' in self.modules:
            result = self.modules['green_mining'].optimize_mining(power_needed_kw, urgency)
            
            # Ажурирај метрики
            if 'block_metrics' in self.modules:
                try:
                    self.modules['block_metrics'].update_metrics({
                        'mining_power': power_needed_kw,
                        'renewable_percentage': result['renewable_percentage'],
                        'carbon_saved': result['carbon_saved_kg']
                    })
                except:
                    pass
            
            return result
        else:
            return {'error': 'Green mining module not available'}
    
    def get_system_status(self):
        """Добиј статус на целиот систем"""
        status = {
            'modules': {},
            'phase1_enabled': self.enabled_features,
            'total_modules': len(self.modules)
        }
        
        for name, module in self.modules.items():
            status['modules'][name] = {
                'type': type(module).__name__,
                'active': True
            }
        
        return status
    
    def run_complete_demo(self):
        """Изврши целосна демонстрација на системот"""
        print("\n" + "="*60)
        print("🎬 АСТРАНЕТ ENHANCED - КОМПЛЕТНА ДЕМОНСТРАЦИЈА")
        print("="*60)
        
        # Демо 1: Трансакциска валидација
        print("\n1. 🔐 ТРАНСАКЦИСКА ВАЛИДАЦИЈА (Quantum + AI)")
        from quantum_validator.quantum_core import create_sample_transaction
        sample_tx = create_sample_transaction()
        valid, msg = self.validate_transaction(sample_tx)
        print(f"   Резултат: {msg}")
        
        # Демо 2: Паметни договори
        print("\n2. 📝 ПАМЕТНИ ДОГОВОРИ (Self-Healing)")
        from self_healing.contract_healer import create_sample_contract
        sample_contract = create_sample_contract()
        contract = self.create_smart_contract(sample_contract, make_self_healing=True)
        
        if hasattr(contract, 'execute'):
            result = contract.execute("transfer", "user1", "user2", 100)
            print(f"   Договор извршен: {result.get('success', 'N/A')}")
        
        # Демо 3: Green Mining
        print("\n3. 🌿 GREEN MINING ОПТИМИЗАЦИЈА")
        mining_result = self.optimize_mining_operation(750, 'medium')
        if 'renewable_percentage' in mining_result:
            print(f"   Обновлива енергија: {mining_result['renewable_percentage']}%")
            print(f"   Заштеда CO2: {mining_result['carbon_saved_kg']}kg")
            print(f"   Трошоци/час: ${mining_result['cost_per_hour']}")
        
        # Демо 4: Системски статус
        print("\n4. 📊 СИСТЕМСКИ СТАТУС")
        status = self.get_system_status()
        print(f"   Активни модули: {status['total_modules']}")
        print(f"   Phase 1 функции: {sum(status['phase1_enabled'].values())}/3")
        
        print("\n" + "="*60)
        print("✅ ДЕМОНСТРАЦИЈАТА ЗАВРШЕНА!")
        print("="*60)

# Функција за лесно користење
def get_enhanced_system():
    """Врати креиран AstraNet Enhanced систем"""
    return AstraNetEnhanced()

# Главна функција за тестирање
if __name__ == "__main__":
    print("🚀 AstraNet Enhanced System")
    print("="*50)
    
    system = AstraNetEnhanced()
    print("\n" + "="*50)
    
    # Прашај го корисникот што сака да направи
    choice = input("\nИзбери опција:\n1. Целосна демонстрација\n2. Само статус\n3. Излез\n\nТвојот избор (1-3): ").strip()
    
    if choice == "1":
        system.run_complete_demo()
    elif choice == "2":
        status = system.get_system_status()
        print(f"\n📊 СИСТЕМСКИ СТАТУС:")
        print(f"   Вкупно модули: {status['total_modules']}")
        for name, info in status['modules'].items():
            print(f"   - {name}: {info['type']}")
    elif choice == "3":
        print("👋 Довидување!")
    else:
        print("❌ Невалиден избор. Стартувам демонстрација...")
        system.run_complete_demo()
