class IndustryInteroperability:
    def integrate(self, shard, industry_name):
        for block in shard:
            block["industry"] = industry_name
        return shard
