import networkx as nx
import urllib.request
import gzip
import os
import time
import matplotlib.pyplot as plt

# Import separated modules
from simulator import estimate_influence
from celf_algo import celf
from ris_algo import ris
from imm_algo import imm
from heuristics import heuristic_high_degree, heuristic_random


# LOADING DATASET
def load_ca_grqc():
    """Downloads and loads the ca-GrQc graph."""
    file_path = "ca-GrQc.txt.gz"
    url = "https://snap.stanford.edu/data/ca-GrQc.txt.gz"
    
    if not os.path.exists(file_path):
        print("Downloading ca-GrQc dataset from SNAP (~1MB)...")
        urllib.request.urlretrieve(url, file_path)
    
    print("Loading graph into memory...")
    G = nx.read_edgelist(file_path, create_using=nx.DiGraph(), nodetype=int, comments='#')
    
    P_VAL = 0.05
    for u, v in G.edges():
        G[u][v]['p'] = P_VAL
        
    print(f"Graph loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges.\n")
    return G, P_VAL


if __name__ == "__main__":
    G, P = load_ca_grqc()
    
    K_VALUES = [5, 10, 15, 20]
    MC_ROUNDS = 100 # Evaluator rounds
    
    # Storage for plotting
    results = {
        "CELF": [],
        "RIS": [],
        "IMM": [],
        "High Degree": [],
        "Random": []
    }
    
    print(f"{'k (Seeds)':<10} | {'CELF Spread':<15} | {'RIS Spread':<15} | {'IMM Spread':<15} | {'Degree Spread':<15} | {'Random Spread':<15}")
    print("-" * 95)
    
    for k in K_VALUES:
        # Generate seeds
        seeds_celf = celf(G, k, p=P, R=30)
        seeds_ris = ris(G, k, p=P, mc_samples=10000)
        seeds_imm = imm(G, k, p=P, epsilon=0.2)
        seeds_deg = heuristic_high_degree(G, k)
        seeds_rand = heuristic_random(G, k)
        
        # Evaluate expected spread uniformly
        spread_celf = estimate_influence(G, seeds_celf, p=P, R=MC_ROUNDS)
        spread_ris = estimate_influence(G, seeds_ris, p=P, R=MC_ROUNDS)
        spread_imm = estimate_influence(G, seeds_imm, p=P, R=MC_ROUNDS)
        spread_deg = estimate_influence(G, seeds_deg, p=P, R=MC_ROUNDS)
        spread_rand = estimate_influence(G, seeds_rand, p=P, R=MC_ROUNDS)
        
        # Store for plotting
        results["CELF"].append(spread_celf)
        results["RIS"].append(spread_ris)
        results["IMM"].append(spread_imm)
        results["High Degree"].append(spread_deg)
        results["Random"].append(spread_rand)
        
        # Print table row
        print(f"{k:<10} | {spread_celf:<15.1f} | {spread_ris:<15.1f} | {spread_imm:<15.1f} | {spread_deg:<15.1f} | {spread_rand:<15.1f}")

    print("\nVerification Complete: CELF, RIS, and IMM should consistently outperform High Degree and Random heuristics.")

    # PLOTTING RESEARCH BENCHMARK
    plt.figure(figsize=(10, 6))
    plt.plot(K_VALUES, results["CELF"], marker='o', label="CELF (Greedy Approx)", linewidth=2)
    plt.plot(K_VALUES, results["RIS"], marker='s', label="RIS", linewidth=2)
    plt.plot(K_VALUES, results["IMM"], marker='^', label="IMM", linewidth=2)
    plt.plot(K_VALUES, results["High Degree"], marker='x', linestyle='--', label="High Degree", linewidth=2)
    plt.plot(K_VALUES, results["Random"], marker='d', linestyle=':', label="Random Selection", linewidth=2)
    
    plt.title("Expected Influence Spread vs. Seed Set Size (ca-GrQc Dataset)")
    plt.xlabel("Seed Set Size (k)")
    plt.ylabel("Expected Spread (Activated Nodes)")
    plt.xticks(K_VALUES)
    plt.legend()
    plt.grid(True)
    
    # Save the plot
    plt.savefig("im_benchmark_results.png")
    print("Graph saved as 'im_benchmark_results.png'")