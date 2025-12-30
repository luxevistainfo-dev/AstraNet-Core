class TxAuditAI:
    def risk_score(self, tx):
        score = 0.0
        if tx.amount > 1000:
            score += 0.6
        if tx.sender == tx.receiver:
            score += 0.4
        return min(score, 1.0)
