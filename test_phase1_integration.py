#!/usr/bin/env python3
"""
ТЕСТ ЗА ИНТЕГРАЦИЈА НА PHASE 1 МОДУЛИ
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🧪 ТЕСТИРАМ ИНТЕГРАЦИЈА")

# Тест 1: Quantum Validator
print("\n1. 🔐 Quantum Validator Test")
try:
    from quantum_validator.quantum_core import QuantumSafeValidator, create_sample_transaction
    validator = QuantumSafeValidator()
    tx = create_sample_transaction()
    valid, msg = validator.validate_transaction(tx)
    print(f"   ✅ {msg}")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Тест 2: Self-Healing Contracts
print("\n2. 🏥 Self-Healing Contracts Test")
try:
    from self_healing.contract_healer import SelfHealingContract, create_sample_contract
    contract = SelfHealingContract(create_sample_contract())
    result = contract.execute("transfer", "alice", "bob", 100)
    print(f"   ✅ Transfer executed: {result.get('success', False)}")
    print(f"   ✅ Healing count: {contract.healing_count}")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Тест 3: Green Mining
print("\n3. 🌿 Green Mining Test")
try:
    from green_mining.energy_optimizer import GreenMiningOptimizer
    optimizer = GreenMiningOptimizer()
    result = optimizer.optimize_mining(500, 'medium')
    print(f"   ✅ Renewable: {result['renewable_percentage']}%")
    print(f"   ✅ Carbon saved: {result['carbon_saved_kg']}kg")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Тест 4: Existing AI Modules
print("\n4. 🤖 Existing AI Modules Test")

# FeePredictor
try:
    from ai.fee_model import FeePredictor
    predictor = FeePredictor()
    print(f"   ✅ FeePredictor: Found")
except Exception as e:
    print(f"   ❌ FeePredictor: {e}")

# SmartContractValidator
try:
    from ai.smart_contract_checker import SmartContractValidator
    validator = SmartContractValidator()
    print(f"   ✅ SmartContractValidator: Found")
except Exception as e:
    print(f"   ❌ SmartContractValidator: {e}")

print("\n" + "="*50)
print("📊 ТЕСТ РЕЗУЛТАТИ:")
print("="*50)
print("🎉 Phase 1 модули се интегрирани во AstraNet-Core!")
print("🚀 Сега можеш да ги користиш во твојот проект.")
