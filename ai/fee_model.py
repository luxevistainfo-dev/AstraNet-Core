# ai/fee_model.py
import numpy as np
from collections import deque
import json
from datetime import datetime

class FeePredictor:
    def __init__(self, window_size=20):
        self.fee_history = deque(maxlen=window_size)
        self.prediction_history = []
    
    def predict_next_fee(self, mempool_size=0, network_congestion=0.5, urgency="normal"):
        if not self.fee_history:
            predicted = 0.1
        else:
            recent_fees = list(self.fee_history)
            predicted = np.mean(recent_fees[-5:]) if len(recent_fees) >= 5 else np.mean(recent_fees)
        
        congestion_factor = 1 + (network_congestion * 2)
        mempool_factor = 1 + min(mempool_size / 200, 2)
        
        urgency_factors = {"low": 0.8, "normal": 1.0, "high": 1.5, "urgent": 3.0}
        urgency_factor = urgency_factors.get(urgency, 1.0)
        
        final_fee = predicted * congestion_factor * mempool_factor * urgency_factor
        final_fee = max(0.01, min(10.0, final_fee))
        
        return round(final_fee, 4)
    
    def add_fee_data(self, block_fees):
        if block_fees:
            avg_fee = sum(block_fees) / len(block_fees)
            self.fee_history.append(avg_fee)
    
    def get_fee_advice(self, transaction_value=0, time_sensitivity="normal"):
        predicted_fee = self.predict_next_fee(50, 0.5, time_sensitivity)
        
        advice = {
            "recommended_fee": predicted_fee,
            "time_sensitivity": time_sensitivity,
            "estimated_confirmation_time": "3-5 blocks" if predicted_fee > 1.0 else "6-10 blocks"
        }
        
        return advice

def test_fee_predictor():
    print("Testing FeePredictor...")
    predictor = FeePredictor()
    
    test_fees = [0.1, 0.15, 0.12, 0.18, 0.2]
    for fee in test_fees:
        predictor.add_fee_data([fee])
    
    fee = predictor.predict_next_fee(100, 0.7, "normal")
    print(f"Predicted fee: {fee}")
    
    advice = predictor.get_fee_advice(500, "normal")
    print(f"Fee advice: {advice}")
    
    print("Test completed!")

if __name__ == "__main__":
    test_fee_predictor()
