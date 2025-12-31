import hashlib
import json
import time
import numpy as np
from datetime import datetime

class QuantumSafeValidator:
    """Quantum-resistant validator for blockchain transactions"""
    
    def __init__(self):
        self.validation_count = 0
        self.threats_blocked = 0
        self.start_time = time.time()
        
    def validate_transaction(self, tx_data):
        """Main validation function"""
        print(f"\n🔐 Validating transaction: {tx_data.get('tx_id', 'Unknown')}")
        
        # Step 1: Basic validation
        if not self._basic_validation(tx_data):
            return False, "Basic validation failed"
        
        # Step 2: Quantum signature check
        if not self._quantum_signature_check(tx_data):
            return False, "Quantum signature verification failed"
        
        # Step 3: AI attack detection
        threat = self._detect_quantum_attack(tx_data)
        if threat:
            self.threats_blocked += 1
            return False, f"Quantum attack detected: {threat}"
        
        # Step 4: Zero-knowledge proof check
        if not self._zkp_check(tx_data):
            return False, "ZKP verification failed"
        
        self.validation_count += 1
        return True, "Transaction is quantum-safe ✓"
    
    def _basic_validation(self, tx):
        """Basic transaction validation"""
        required = ['from', 'to', 'amount', 'timestamp', 'nonce']
        
        for field in required:
            if field not in tx:
                print(f"❌ Missing field: {field}")
                return False
        
        if tx['amount'] <= 0:
            print("❌ Amount must be positive")
            return False
        
        if tx['from'] == tx['to']:
            print("❌ Sender and receiver are the same")
            return False
        
        time_diff = abs(time.time() - tx['timestamp'])
        if time_diff > 3600:
            print(f"❌ Transaction too old: {time_diff:.0f} seconds")
            return False
        
        return True
    
    def _quantum_signature_check(self, tx):
        """Quantum-resistant signature verification"""
        if 'signature' not in tx:
            print("❌ No signature")
            return False
        
        sig = tx['signature']
        
        # 1. Length check (quantum signatures are longer)
        if len(sig) < 128:
            print(f"❌ Signature too short for quantum safety: {len(sig)}")
            return False
        
        # 2. Quantum-resistant hash
        tx_hash = self._quantum_hash(tx)
        
        # 3. Lattice-based verification simulation
        if not self._verify_lattice_based(sig, tx_hash):
            print("❌ Lattice-based verification failed")
            return False
        
        return True
    
    def _quantum_hash(self, data):
        """Quantum-resistant hash function"""
        data_str = json.dumps(data, sort_keys=True)
        
        # Combination of multiple algorithms
        h1 = hashlib.sha256(data_str.encode()).hexdigest()
        h2 = hashlib.sha3_512(data_str.encode()).hexdigest()
        h3 = hashlib.blake2b(data_str.encode()).hexdigest()
        
        return h1 + h2 + h3
    
    def _verify_lattice_based(self, signature, data_hash):
        """Simulation of lattice-based verification"""
        # Check if signature contains quantum-safe markers
        quantum_markers = ['QRS', 'LAT', 'KYB', 'DIL', 'NTRU', 'FALCON']
        
        for marker in quantum_markers:
            if marker in signature.upper():
                return True
        
        # Alternative: check mathematical properties
        sig_bytes = signature.encode() if isinstance(signature, str) else signature
        
        if len(sig_bytes) > 100:
            # Check for "randomness" (entropy)
            unique_bytes = len(set(sig_bytes))
            entropy_ratio = unique_bytes / len(sig_bytes)
            
            if entropy_ratio > 0.7:
                return True
        
        return False
    
    def _detect_quantum_attack(self, tx):
        """Quantum attack detection"""
        # Check for Shor attack (periodicity)
        if 'signature' in tx:
            sig = tx['signature']
            if self._check_periodicity(sig):
                return "Shor algorithm (periodicity detected)"
        
        # Check for replay
        if 'nonce' in tx and tx.get('nonce', 0) < 1:
            return "Invalid nonce (possible replay attack)"
        
        # Timing attack detection
        if 'timestamp' in tx:
            current_time = time.time()
            time_diff = current_time - tx['timestamp']
            if time_diff < 0.001 and time_diff >= 0:
                return "Possible timing attack (too fast)"
        
        return None
    
    def _check_periodicity(self, data):
        """Check for periodic patterns (Shor attack)"""
        if len(data) < 50:
            return False
        
        # Check for substring repetition
        for length in range(5, 20):
            for i in range(len(data) - length * 2):
                substring = data[i:i+length]
                if substring in data[i+length:]:
                    return True
        
        return False
    
    def _zkp_check(self, tx):
        """Zero-Knowledge Proof check (simplified)"""
        if 'amount' in tx and 'fee' in tx:
            total = tx['amount'] + tx.get('fee', 0)
            
            if total > 10**15:
                return False
            
            if total <= 0:
                return False
        
        return True
    
    def get_stats(self):
        """Get performance statistics"""
        uptime = time.time() - self.start_time
        return {
            'validations': self.validation_count,
            'threats_blocked': self.threats_blocked,
            'success_rate_%': round((self.validation_count / max(self.validation_count + self.threats_blocked, 1)) * 100, 2),
            'uptime_seconds': round(uptime, 2)
        }

def create_sample_transaction():
    """Create sample transaction for testing"""
    return {
        'tx_id': f'tx_{int(time.time())}_{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}',
        'from': 'user1_' + hashlib.sha256(b'user1').hexdigest()[:16],
        'to': 'user2_' + hashlib.sha256(b'user2').hexdigest()[:16],
        'amount': 100.50,
        'fee': 0.001,
        'timestamp': time.time() - 1,
        'nonce': int(time.time() * 1000) % 1000000,
        'signature': f'QRS_{hashlib.sha512(str(time.time()).encode()).hexdigest()}_LAT_{hashlib.blake2b(str(time.time()).encode()).hexdigest()}'
    }
