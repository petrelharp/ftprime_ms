"""
Code for investigating the space complexity of algorithm W along
with serial simplification.
"""
import random
import numpy as np
import msprime

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns


def wright_fisher(N, T, simplify_interval=1):
    """
    An implementation of algorithm W where we simplify after every generation.
    The goal here is to measure the number of edges in the tree sequence
    representing the history as a function of time.

    For simplicity we assume that the genome length L = 1 and the probability
    of death delta = 1.
    """
    L = 1
    edges = msprime.EdgeTable()
    nodes = msprime.NodeTable()
    P = [j for j in range(N)]
    for j in range(N):
        nodes.add_row(time=T, flags=1)
    t = T
    S = np.zeros(T, dtype=int)
    L = np.zeros(T, dtype=float)
    while t > 0:
        t -= 1
        Pp = [P[j] for j in range(N)]
        for j in range(N):
            n = len(nodes)
            nodes.add_row(time=t, flags=1)
            Pp[j] = n
            a = random.randint(0, N - 1)
            b = random.randint(0, N - 1)
            x = random.uniform(0, L)
            edges.add_row(0, x, P[a], n)
            edges.add_row(x, L, P[b], n)
        P = Pp
        if t % simplify_interval == 0:
            msprime.sort_tables(nodes=nodes, edges=edges)
            msprime.simplify_tables(Pp, nodes, edges)
            P = list(range(N))
        S[T - t - 1] = len(edges)
        L[T - t - 1] = total_length(nodes, edges)
    # We will always simplify at t = 0, so no need for special case at the end
    return msprime.load_tables(nodes=nodes, edges=edges), S, L

def total_length(nodes, edges):
    ts = msprime.load_tables(nodes=nodes, edges=edges)
    L = 0.0
    for t in ts.trees():
        L += t.length * t.total_branch_length
    return L

def verify():
    """
    Crude check to see if we get the same result when we serial simplify and we
    don't.
    """
    for seed in range(1, 10):
        for n in [5, 10, 20]:
            for T in [1, 10, 100]:
                print("Checking ", n, T, seed)
                random.seed(seed)
                ts1, _, _ = wright_fisher(n, T, T + 1)
                random.seed(seed)
                ts2, _, _ = wright_fisher(n, T, 1)
                assert ts1.tables.nodes == ts2.tables.nodes
                assert ts1.tables.edges == ts2.tables.edges

def plot():
    num_reps = 10
    for n in [10, 100, 1000]:
        T = 10 * n
        A = np.zeros((num_reps, T))
        B = np.zeros((num_reps, T))
        for j in range(num_reps):
            _, S, L = wright_fisher(n, T)
            A[j] = S
            B[j] = L
            plt.subplot(211)
            plt.plot(S, alpha=0.5)
            plt.subplot(212)
            plt.plot(L, alpha=0.5)
            print(n, j, "done")
        mean_S = np.mean(A, axis=0)
        mean_L = np.mean(B, axis=0)
        plt.subplot(211)
        plt.plot(mean_S, color="black", lw=3)
        plt.title("N = {}".format(n))
        plt.xlabel("Generations")
        plt.ylabel("Number of edges")
        plt.subplot(212)
        plt.plot(mean_L, color="black", lw=3)
        plt.title("N = {}".format(n))
        plt.xlabel("Generations")
        plt.ylabel("Total tree length")
        plt.savefig("{}.png".format(n))
        plt.clf()



if __name__ == "__main__":
    # verify()
    plot()
