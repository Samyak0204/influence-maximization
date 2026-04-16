import heapq
from simulator import estimate_influence

def celf(G, k, p=0.05, R=50):
    """Leskovec et al. optimized greedy using submodularity."""
    q = []
    for v in G.nodes():
        gain = estimate_influence(G, [v], p, R=10) # Fast initial pass
        heapq.heappush(q, (-gain, v, 0))

    S = []
    spread = 0
    
    while len(S) < k:
        gain, v, iteration = heapq.heappop(q)
        if iteration == len(S):
            S.append(v)
            spread += -gain
        else:
            new_gain = estimate_influence(G, S + [v], p, R) - spread
            heapq.heappush(q, (-new_gain, v, len(S)))
            
    return S