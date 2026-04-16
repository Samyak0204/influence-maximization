import random

def heuristic_high_degree(G, k):
    """Baseline 1: Pick nodes with the highest out-degree."""
    degrees = dict(G.out_degree())
    sorted_nodes = sorted(degrees.keys(), key=lambda x: degrees[x], reverse=True)
    return sorted_nodes[:k]

def heuristic_random(G, k):
    """Baseline 2: Pick nodes entirely at random."""
    return random.sample(list(G.nodes()), k)