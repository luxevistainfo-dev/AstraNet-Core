#!/usr/bin/env python3
"""
ENHANCED NODE.PY - AstraNet Core Node со Phase 1 интегрирани модули
"""

import sys
import os
import time
import json
from datetime import datetime

# Додади го интегрираниот систем
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class EnhancedNode:
    """Подобрена верзија на Node со Phase 1 модули"""
    
    def __init__(self, node_id, network='testnet'):
        self.node_id = node_id
        self.network = network
        self.start_time = time.time()
        self.transactions = []
        self.blocks = []
        
        # Иницијализирај го интегрираниот систем
        print(f"🚀 Иницијализирам Enhanced Node {node_id}...")
        
        try:
            # Користи го интегрираниот систем
            from astranet_enhanced import AstraNetEnhanced
            self.enhanced_system = AstraNetEnhanced()
            print("✅ AstraNet Enhanced систем инсталиран")
        except ImportError as e:
            print(f"⚠️ AstraNet Enhanced не е достапен: {e}")
            self.enhanced_system = None
        
        # Постоечки функции
        self._init_core_functions()
    
    def _init_core_functions(self):
        """Иницијализирај ги основните функции"""
        print("🔧 Иницијализирам основни функции...")
        
        # Овде би ги иницијализирал постоечките функции од оригиналниот node.py
        # За сега креирај празни функции
    
    def process_transaction(self, tx_data):
        """Обработи трансакција со enhanced валидација"""
        print(f"\n🔍 Обработка на трансакција на Node {self.node_id}")
        
        if self.enhanced_system:
            # Користи enhanced валидација
            is_valid, message = self.enhanced_system.validate_transaction(tx_data)
            
            if is_valid:
                self.transactions.append({
                    **tx_data,
                    'validated_by': 'enhanced_system',
                    'timestamp': time.time(),
                    'node_id': self.node_id
                })
                print(f"✅ Трансакцијата е валидна: {message}")
                return True
            else:
                print(f"❌ Трансакцијата не е валидна: {message}")
                return False
        else:
            # Основна валидација
            if all(k in tx_data for k in ['from', 'to', 'amount']):
                self.transactions.append(tx_data)
                print("✅ Трансакцијата е прифатена (basic validation)")
                return True
            else:
                print("❌ Трансакцијата е невалидна (basic validation)")
                return False
    
    def deploy_contract(self, contract_code, contract_id):
        """Деплојрај договор со self-healing способности"""
        print(f"\n📝 Деплојрам договор {contract_id}")
        
        if self.enhanced_system:
            contract = self.enhanced_system.create_smart_contract(contract_code, make_self_healing=True)
            
            # Зачувај го договорот
            contract_info = {
                'id': contract_id,
                'deployed_at': time.time(),
                'node': self.node_id,
                'type': 'self_healing' if hasattr(contract, 'execute') else 'basic',
                'contract': contract
            }
            
            # Додај во блокчејн (симулација)
            self.blocks.append({
                'type': 'contract_deployment',
                'contract_id': contract_id,
                'timestamp': time.time()
            })
            
            print(f"✅ Договорот {contract_id} е деплоиран")
            if hasattr(contract, 'healing_count'):
                print(f"   Self-healing способности: АКТИВНИ")
            
            return contract_info
        else:
            print("⚠️ Enhanced систем не е достапен, користам basic договор")
            return {'id': contract_id, 'type': 'basic', 'code': contract_code}
    
    def mine_block(self, transactions=None, mining_power=500):
        """Ископaj блок со green mining оптимизација"""
        print(f"\n⛏️  Копање блок на Node {self.node_id}")
        
        if self.enhanced_system:
            # Оптимизирај mining
            mining_result = self.enhanced_system.optimize_mining_operation(mining_power, 'medium')
            
            # Креирај блок
            new_block = {
                'block_id': f"block_{int(time.time())}_{self.node_id}",
                'timestamp': time.time(),
                'miner': self.node_id,
                'transactions': transactions or self.transactions[-10:],  # Последни 10 трансакции
                'mining_stats': mining_result,
                'size': len(json.dumps(transactions or [])) if transactions else 0
            }
            
            self.blocks.append(new_block)
            self.transactions = []  # Исчисти ги обработените трансакции
            
            print(f"✅ Блок {new_block['block_id']} ископан")
            print(f"   Обновлива енергија: {mining_result.get('renewable_percentage', 'N/A')}%")
            print(f"   Заштеда CO2: {mining_result.get('carbon_saved_kg', 'N/A')}kg")
            
            return new_block
        else:
            # Basic mining
            new_block = {
                'block_id': f"block_{int(time.time())}_{self.node_id}",
                'timestamp': time.time(),
                'miner': self.node_id,
                'transactions': transactions or []
            }
            
            self.blocks.append(new_block)
            print(f"✅ Блок {new_block['block_id']} ископан (basic mining)")
            
            return new_block
    
    def get_node_stats(self):
        """Добиј статистики за јазолот"""
        uptime = time.time() - self.start_time
        
        stats = {
            'node_id': self.node_id,
            'network': self.network,
            'uptime_seconds': round(uptime, 2),
            'uptime_hours': round(uptime / 3600, 2),
            'transactions_processed': len(self.transactions),
            'blocks_mined': len(self.blocks),
            'enhanced_system': 'ACTIVE' if self.enhanced_system else 'INACTIVE',
            'phase1_features': ['quantum_validation', 'self_healing_contracts', 'green_mining'] if self.enhanced_system else []
        }
        
        if self.enhanced_system:
            try:
                system_status = self.enhanced_system.get_system_status()
                stats['enhanced_modules'] = system_status['total_modules']
            except:
                stats['enhanced_modules'] = 'UNKNOWN'
        
        return stats
    
    def run_demo(self):
        """Изврши демонстрација на enhanced јазол"""
        print("\n" + "="*60)
        print(f"🎬 ENHANCED NODE {self.node_id} - ДЕМОНСТРАЦИЈА")
        print("="*60)
        
        # Демо 1: Трансакции
        print("\n1. 🔄 ОБРАБОТКА НА ТРАНСАКЦИИ")
        from quantum_validator.quantum_core import create_sample_transaction
        sample_tx = create_sample_transaction()
        self.process_transaction(sample_tx)
        
        # Демо 2: Договори
        print("\n2. 📝 ДЕПЛОЈ НА ДОГОВОРИ")
        from self_healing.contract_healer import create_sample_contract
        sample_contract = create_sample_contract()
        self.deploy_contract(sample_contract, "demo_contract_001")
        
        # Демо 3: Mining
        print("\n3. ⛏️  MINING НА БЛОК")
        self.mine_block(mining_power=600)
        
        # Демо 4: Статистики
        print("\n4. 📊 СТАТИСТИКИ")
        stats = self.get_node_stats()
        print(f"   Јазол ID: {stats['node_id']}")
        print(f"   Трансакции: {stats['transactions_processed']}")
        print(f"   Блокови: {stats['blocks_mined']}")
        print(f"   Phase 1 функции: {len(stats['phase1_features'])}/3")
        
        print("\n" + "="*60)
        print("✅ ДЕМОНСТРАЦИЈАТА ЗАВРШЕНА!")
        print("="*60)

# Главна функција
def main():
    """Главна функција за тестирање"""
    print("🚀 AstraNet Enhanced Node System")
    print("="*50)
    
    # Креирај enhanced јазол
    node = EnhancedNode("enhanced_node_001", "testnet")
    
    # Прашај го корисникот
    choice = input("\nИзбери опција:\n1. Демонстрација\n2. Статистики\n3. Излез\n\nТвојот избор (1-3): ").strip()
    
    if choice == "1":
        node.run_demo()
    elif choice == "2":
        stats = node.get_node_stats()
        print(f"\n📊 СТАТИСТИКИ ЗА ЈАЗОЛ {stats['node_id']}:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
    elif choice == "3":
        print("👋 Довидување!")
    else:
        print("❌ Невалиден избор")

if __name__ == "__main__":
    main()
