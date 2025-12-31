from core.blockchain import Blockchain
from core.validator import QuantumResistantValidator
from ai.ai_engine import AIEngine
from ai.self_healing import SelfHealingEngine
from ai.green_optimizer import GreenMiningOptimizer
from core.sharding import ShardingManager
from modules.cross_chain import CrossChainBridge
from modules.marketplace import Marketplace

chain = Blockchain()
validator = QuantumResistantValidator()
ai = AIEngine()
healer = SelfHealingEngine()
green = GreenMiningOptimizer()
sharder = ShardingManager()
bridge = CrossChainBridge()
market = Marketplace()

chain.add_block("Normal transaction")
chain.add_block("Error in contract")

exported = chain.export()

for block in exported:
    ai.analyze(block)
    healer.heal(block)

is_valid = validator.validate(chain.chain[-1].hash)
shard_a, shard_b = sharder.shard(exported)

print("VALID:", is_valid)
print("GREEN:", green.optimize())
print("CROSS:", bridge.relay("AstraNet payload"))
print("MARKET:", market.list_service("AI Validator", 5))
