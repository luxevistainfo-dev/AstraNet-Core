class BlockFilterAI:
    def approve_block(self, risk_avg):
        return risk_avg < 0.7
