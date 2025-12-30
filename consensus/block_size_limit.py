# consensus/block_size_limit.py

def block_size_limit(mempool):
    """
    Големината на блокот се менува според мемпул.
    """
    if len(mempool.transactions) < 10:
        return 2
    elif len(mempool.transactions) < 50:
        return 5
    return 10

