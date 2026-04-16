import random

def ic_simulator(G, seed_set, p=0.05):
    """Simulates the IC model once and returns the number of activated nodes."""
    active_nodes = set(seed_set)
    newly_active = list(seed_set)
    
    while newly_active:
        next_round = []
        for u in newly_active:
            for v in G.successors(u):
                if v not in active_nodes:
                    prob = G[u][v].get('p', p)
                    if random.random() < prob:
                        active_nodes.add(v)
                        next_round.append(v)
        newly_active = next_round
    return len(active_nodes)

def estimate_influence(G, seed_set, p=0.05, R=50):
    """Monte Carlo estimation of spread over R iterations."""
    if not seed_set: return 0
    return sum(ic_simulator(G, seed_set, p) for _ in range(R)) / R