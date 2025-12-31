class AIEngine:
    def analyze(self, block):
        risk = len(block.hash) % 10
        return {"risk": risk, "status": "OK" if risk < 7 else "RISK"}
