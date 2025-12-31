from core.blockchain import Blockchain, Block
from core.transaction import Transaction
from core.mempool import Mempool
from core.validator import QuantumResistantValidator
from core.sharding import ShardingManager
from core.node import Node
from ai.ai_engine import AIEngine
from ai.self_healing import SelfHealingEngine
from ai.green_optimizer import GreenMiningOptimizer
from modules.cross_chain import CrossChainBridge
from modules.marketplace import Marketplace
import threading

# Blockchain + Mempool
blockchain = Blockchain()
mempool = Mempool()

# Nodes (Local Testnet)
node1 = Node('127.0.0.1', 5001)
node2 = Node('127.0.0.1', 5002)

# AI + Self-Healing + Green
ai = AIEngine()
healer = SelfHealingEngine()
green = GreenMiningOptimizer()

# Cross-Chain + Marketplace
bridge = CrossChainBridge()
market = Marketplace()

# Validator + Sharding
validator = QuantumResistantValidator()
sharder = ShardingManager()

# Start nodes in background threads
t1 = threading.Thread(target=node1.start, daemon=True)
t2 = threading.Thread(target=node2.start, daemon=True)
t1.start()
t2.start()

# Create transactions
mempool.add_transaction(Transaction("Alice", "Bob", 10))
mempool.add_transaction(Transaction("Bob", "Charlie", 5))

txs = mempool.get_transactions()
nonce, block_hash = blockchain.mine_block()

block = Block(
    index=len(blockchain.chain),
    previous_hash=blockchain.chain[-1].hash,
    transactions=[tx.__dict__ for tx in txs],
    nonce=nonce,
    hash=block_hash
)

blockchain.chain.append(block)

# AI Analysis + Self-Healing
for b in blockchain.chain:
    ai.analyze(b)
    healer.heal(b)

# Validator + Sharding
is_valid = validator.validate(blockchain.chain[-1].hash)
shard_a, shard_b = sharder.shard([b.__dict__ for b in blockchain.chain])

# Print results
print("NEW BLOCK MINED:", block.__dict__)
print("VALID:", is_valid)
print("GREEN:", green.optimize())
print("CROSS:", bridge.relay("AstraNet payload"))
print("MARKET:", market.list_service("AI Validator", 5))
print("SHARD A:", shard_a)
print("SHARD B:", shard_b)
