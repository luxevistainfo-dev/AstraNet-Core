import numpy as np
import hashlib
import json
import time

class QuantumAIDetector:
    """AI system for quantum attack detection"""
    
    def __init__(self):
        self.pattern_database = self._load_patterns()
        self.threshold = 0.7
        
    def _load_patterns(self):
        """Load known attack patterns"""
        return {
            'shor_pattern': self._create_shor_pattern(),
            'grover_pattern': self._create_grover_pattern(),
            'bruteforce_pattern': self._create_bruteforce_pattern()
        }
    
    def analyze_transaction(self, tx_data):
        """Analyze transaction for quantum attacks"""
        risk_score = 0
        detected_threats = []
        
        if 'signature' in tx_data:
            sig_risk = self._analyze_signature(tx_data['signature'])
            risk_score += sig_risk['score']
            if sig_risk['threat']:
                detected_threats.append(sig_risk['threat'])
        
        time_risk = self._analyze_timing(tx_data)
        risk_score += time_risk
        
        data_risk = self._analyze_data_patterns(tx_data)
        risk_score += data_risk
        
        ml_prediction = self._ml_predict(tx_data)
        risk_score += ml_prediction * 20
        
        risk_percentage = min(100, risk_score)
        
        if risk_percentage > 80:
            threat_level = "HIGH"
            action = "BLOCK"
        elif risk_percentage > 50:
            threat_level = "MEDIUM"
            action = "REVIEW"
        else:
            threat_level = "LOW"
            action = "ALLOW"
        
        return {
            'risk_score': risk_percentage,
            'threat_level': threat_level,
            'action': action,
            'detected_threats': detected_threats,
            'timestamp': time.time()
        }
    
    def _analyze_signature(self, signature):
        """AI-based signature analysis"""
        score = 0
        threat = None
        
        sig_len = len(str(signature))
        if sig_len < 100:
            score += 30
            threat = "Signature too short for quantum safety"
        
        entropy = self._calculate_entropy(str(signature))
        if entropy < 4.0:
            score += 25
            threat = "Low entropy (possibly predictable)"
        
        quantum_markers = ['QRS', 'LAT', 'KYB', 'DIL', 'NTRU', 'FALCON']
        has_marker = any(marker in str(signature).upper() for marker in quantum_markers)
        
        if not has_marker:
            score += 20
            threat = "No quantum-safe markers"
        
        return {'score': score, 'threat': threat}
    
    def _calculate_entropy(self, data):
        """Calculate information entropy"""
        if not data:
            return 0
        
        prob = [float(data.count(c)) / len(data) for c in set(data)]
        entropy = -sum([p * np.log2(p) for p in prob if p > 0])
        return entropy
    
    def _analyze_timing(self, tx_data):
        """Timing characteristics analysis"""
        score = 0
        
        if 'timestamp' in tx_data:
            current_time = time.time()
            time_diff = abs(current_time - tx_data['timestamp'])
            
            if time_diff < 0.1:
                score += 40
            elif time_diff > 86400:
                score += 30
        
        return score
    
    def _analyze_data_patterns(self, tx_data):
        """Data pattern analysis"""
        score = 0
        
        if tx_data.get('from', '').startswith('0x') and tx_data.get('to', '').startswith('0x'):
            if tx_data['from'][2:10] == tx_data['to'][2:10]:
                score += 25
        
        amount = tx_data.get('amount', 0)
        if amount == 0 or amount > 10**9:
            score += 15
        
        return score
    
    def _ml_predict(self, tx_data):
        """ML prediction simulation"""
        features = []
        
        if 'signature' in tx_data:
            features.append(len(tx_data['signature']) / 1000)
            features.append(self._calculate_entropy(str(tx_data['signature'])) / 8)
        
        if 'amount' in tx_data:
            features.append(min(1, tx_data['amount'] / 1000000))
        
        if len(features) > 0:
            return sum(features) / len(features)
        
        return 0.5
    
    def _create_shor_pattern(self):
        return {'type': 'periodic', 'risk': 85}
    
    def _create_grover_pattern(self):
        return {'type': 'oscillation', 'risk': 75}
    
    def _create_bruteforce_pattern(self):
        return {'type': 'repetition', 'risk': 65}
