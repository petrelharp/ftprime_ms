"""
Simulation of WF model and output resulting tree sequence.
"""
import random
import msprime

def wright_fisher(N, delta, L, T):
    """
    Direct implementation of Algorithm W.
    """
    edges = msprime.EdgeTable()
    tau = []
    P = [j for j in range(N)]
    for j in range(N):
        tau.append(T)
    t = T
    n = N
    while t > 0:
        t -= 1
        j = 0
        Pp = [P[j] for j in range(N)]
        while j < N:
            if random.random() < delta:
                Pp[j] = n
                tau.append(t)
                a = random.randint(0, N - 1)
                b = random.randint(0, N - 1)
                x = random.uniform(0, L)
                edges.add_row(0, x, P[a], n)
                edges.add_row(x, L, P[b], n)
                n += 1
            j += 1
        P = Pp
    nodes = msprime.NodeTable()
    P = set(P)
    for j in range(n):
        nodes.add_row(time=tau[j], flags=int(j in P))
    msprime.sort_tables(nodes=nodes, edges=edges)
    return msprime.load_tables(nodes=nodes, edges=edges)
