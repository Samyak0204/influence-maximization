from simulator import estimate_influence

def greedy(G, k, p=0.05, R=50):
    """Kempe et al. standard greedy approach."""
    S = []
    for _ in range(k):
        best_node = None
        max_gain = -1
        for v in G.nodes():
            if v not in S:
                gain = estimate_influence(G, S + [v], p, R)
                if gain > max_gain:
                    max_gain = gain
                    best_node = v
        S.append(best_node)
    return S