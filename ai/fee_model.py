class FeeAI:
    def calculate_fee(self, mempool_size):
        base_fee = 0.01
        return base_fee + (mempool_size * 0.001)
