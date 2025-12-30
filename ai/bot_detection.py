class BotDetectorAI:
    def is_bot(self, tx_list):
        senders = [tx.sender for tx in tx_list]
        return len(senders) != len(set(senders))
