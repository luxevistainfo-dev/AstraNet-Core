import hashlib
import secrets

class QuantumResistantValidator:
    def __init__(self):
        self.secret = secrets.token_hex(32)

    def validate(self, block_hash):
        proof = hashlib.sha512((block_hash + self.secret).encode()).hexdigest()
        return proof.startswith("000")
