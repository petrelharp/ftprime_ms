"""
Code for investigating the space complexity of algorithm W along
with serial simplification.
"""
import random
import numpy as np
import msprime

import pandas as pd

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# import seaborn as sns


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
    # We will always simplify at t = 0, so no need for special case at the end
    return msprime.load_tables(nodes=nodes, edges=edges), S

def total_length(nodes, edges):
    ts = msprime.load_tables(nodes=nodes, edges=edges)
    Q = 0.0
    for t in ts.trees():
        Q += t.length * t.total_branch_length
    return Q

def ub(T, N):
    # 2 N \left( 1 + 4 \log\left( \frac{NT}{T + 2 N} \right)\right) .
    # return 2 * (N - 1) + 8 * N * np.log(N/(1+2*N/(T+2)))
    # return 2 * N * (1 + 4 * np.log(N * T / (T + 2 * N)))
    # return 2 * N * (1 + 4 * np.log(N * T / (2 * T + 2 * N)))
    return 2 * N * (1 - (1 / N) + 4 * np.log(min(N,  (T + 2) / 2 )))


def get_mean_edges_per_transition(ts):
    d = np.zeros(ts.num_trees - 1)
    for j, (_, edges_out, edges_in) in enumerate(ts.edge_diffs()):
        if len(edges_out) > 0:
            d[j - 1] = len(edges_in)
    return np.mean(d)


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

    fig = plt.figure()
    ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=2)
    ax2 = plt.subplot2grid((2, 2), (1, 0))
    ax3 = plt.subplot2grid((2, 2), (1, 1))

    num_reps = 10
    n = 50

    T = 15 * n
    A = np.zeros((num_reps, T))
    for j in range(num_reps):
        ts, S = wright_fisher(n, T)
        A[j] = S
        ax1.plot(S, alpha=0.5)
        print(n, j, "done")

    x = [ub(t,n) for t in range(1,T)]
    ax1.plot(x, ls="dashed", color="black", lw=3)
    mean_S = np.mean(A, axis=0)
    ax1.plot(mean_S, lw=3)
    # ax1.set_title("N = {}".format(n))
    ax1.set_title("(A)")
    ax1.set_xlabel("Generations")
    ax1.set_ylabel("Number of edges")

    df = pd.read_csv("data/simplify_num_edges.dat")
    ax2.plot(df.num_edges * 1e-8, df.time)
    ax2.set_xlabel("Number of edges $\\times 10^8$")
    ax2.set_ylabel("Time to simplify (s)")
    ax2.set_title("(B)")

    df = pd.read_csv("data/simplify_subsample.dat")
    ax3.semilogx(df.subsample_size, df.time)
    ax3.set_xlabel("Subsample size")
    ax3.set_title("(C)")

    plt.tight_layout()
    plt.savefig("simplify-results.pdf", format='pdf')



if __name__ == "__main__":
    # verify()
    plot()

