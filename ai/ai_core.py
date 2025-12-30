from ai.tx_audit import TxAuditAI
from ai.bot_detection import BotDetectorAI
from ai.fee_model import FeeAI
from ai.block_filter import BlockFilterAI

class AstraAI:
    def __init__(self):
        self.audit = TxAuditAI()
        self.bot = BotDetectorAI()
        self.fee = FeeAI()
        self.filter = BlockFilterAI()
    
    def analyze_block(self, txs):
        risks = [self.audit.risk_score(tx) for tx in txs]
        avg_risk = sum(risks) / len(risks) if risks else 0
        bot = self.bot.is_bot(txs)
        return avg_risk, bot
