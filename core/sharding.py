class ShardingManager:
    def shard(self, chain):
        mid = len(chain) // 2
        return chain[:mid], chain[mid:]
