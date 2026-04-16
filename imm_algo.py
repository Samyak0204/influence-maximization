import math
import random
from rr_helpers import get_rr_set, max_coverage

def imm(G, k, p=0.05, epsilon=0.2, l=1):
    """Tang et al. IMM Algorithm."""
    n = G.number_of_nodes()
    l_gamma = math.log(n)
    alpha_beta = math.sqrt(l_gamma + math.log(2)) + math.sqrt(l_gamma)
    
    LB = 1 
    nodes = list(G.nodes())
    for i in range(1, int(math.log2(n))):
        x = n / (2 ** i)
        theta_prime = int((2 + 2/3 * epsilon) * (math.log(n) + l * math.log(n) + math.log(math.log2(n))) * n / x)
        rr_sets = [get_rr_set(G, random.choice(nodes), p) for _ in range(theta_prime)]
        S_prime = max_coverage(rr_sets, k)
        
        covered = len(set.union(*[set(rr_sets[idx]) for idx, rr in enumerate(rr_sets) if any(node in rr for node in S_prime)])) if rr_sets else 0
        if covered / theta_prime > 1 / (2 ** i):
            LB = covered / theta_prime * n
            break

    theta = int(2 * n * ((1 - 1/math.e) * alpha_beta + math.sqrt(math.log(n)))**2 / (epsilon**2 * LB))
    theta = min(theta, 30000) # Safety cap for memory limits
    
    final_rr_sets = [get_rr_set(G, random.choice(nodes), p) for _ in range(theta)]
    return max_coverage(final_rr_sets, k)