class ShardingManager:
    def create_shards(self, chain, num_shards):
        shards = [[] for _ in range(num_shards)]
        for i, block in enumerate(chain):
            shards[i % num_shards].append(block.__dict__)
        return shards[0], shards[1]

    def decentralized_train(self, node_name, shard_data):
        model_summary = f"Trained model on {len(shard_data)} blocks for {node_name}"
        return model_summary

