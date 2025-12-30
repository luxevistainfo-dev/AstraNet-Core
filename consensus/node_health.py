# consensus/node_health.py

def node_health(node_metrics):
    """
    AI предвидува дали node ќе се „спржи" или ќе заостанува.
    """
    score = 1 - node_metrics["cpu_load"]/100
    return {"healthy": score>0.5, "score": score}

