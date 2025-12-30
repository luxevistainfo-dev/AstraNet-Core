from core.transaction import Transaction
from core.chain import Blockchain
from core.mempool import Mempool
from ai.ai_core import AstraAI

chain = Blockchain()
ai = AstraAI()

# Create multiple nodes (simulated)
mempools = [Mempool() for _ in range(3)]

# Send transactions to all nodes
txs = [
    Transaction("Alice", "Bob", 100),
    Transaction("Bob", "Charlie", 500),
    Transaction("Charlie", "Alice", 50),
    Transaction("Alice", "Alice", 2000)  # Ризична трансакција
]

for mempool in mempools:
    for tx in txs:
        mempool.add_tx(tx)

# Analyze and mine
for i, mempool in enumerate(mempools):
    risk, bot = ai.analyze_block(mempool.transactions)
    print(f"Node {i} -> Risk: {risk:.2f}, Bot detected: {bot}")
    if not bot and ai.filter.approve_block(risk):
        chain.add_block(mempool.transactions)
        mempool.clear()
        print(f"Node {i}: Block mined successfully!")
    else:
        print(f"Node {i}: Block rejected.")
