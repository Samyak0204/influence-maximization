import random

def get_rr_set(G, v, p=0.05):
    """Generates one Reverse Reachable set from target node v."""
    rr_set = {v}
    active = [v]
    while active:
        u = active.pop()
        for neighbor in G.predecessors(u):
            if neighbor not in rr_set:
                prob = G[neighbor][u].get('p', p)
                if random.random() < prob:
                    rr_set.add(neighbor)
                    active.append(neighbor)
    return rr_set

def max_coverage(rr_sets, k):
    """Greedy Maximum Coverage algorithm on generated RR sets."""
    node_coverage = {}
    for i, rr in enumerate(rr_sets):
        for node in rr:
            if node not in node_coverage:
                node_coverage[node] = set()
            node_coverage[node].add(i)
            
    S = []
    covered_sets = set()
    
    for _ in range(k):
        best_node = None
        max_covered = -1
        
        for node, sets in node_coverage.items():
            if node not in S:
                new_covers = len(sets - covered_sets)
                if new_covers > max_covered:
                    max_covered = new_covers
                    best_node = node
                    
        if best_node is None: break
        S.append(best_node)
        covered_sets.update(node_coverage[best_node])
        
    return S