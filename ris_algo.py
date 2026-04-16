import random
from rr_helpers import get_rr_set, max_coverage

def ris(G, k, p=0.05, mc_samples=10000):
    """Borgs et al. Reverse Influence Sampling."""
    nodes = list(G.nodes())
    rr_sets = [get_rr_set(G, random.choice(nodes), p) for _ in range(mc_samples)]
    return max_coverage(rr_sets, k)