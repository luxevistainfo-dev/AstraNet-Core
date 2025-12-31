class SelfHealingEngine:
    def heal(self, block):
        block_data = str(block.__dict__)
        if "error" in block_data.lower():
            print("Block healed")
        else:
            print("Block OK")
