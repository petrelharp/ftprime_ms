"""
Simulation of WF model and output resulting tree sequence.

Requires msprime >= 0.6.0
"""
import random
import msprime


def wright_fisher(N, delta, L, T):
    """
    Direct implementation of Algorithm W.
    """
    tables = msprime.TableCollection(L)
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
                tables.edges.add_row(0, x, P[a], n)
                tables.edges.add_row(x, L, P[b], n)
                n += 1
            j += 1
        P = Pp
    P = set(P)
    for j in range(n):
        tables.nodes.add_row(time=tau[j], flags=int(j in P))
    tables.sort()
    return tables.tree_sequence()



if __name__ == "__main__":

    random.seed(2)
    ts = wright_fisher(5, 0.95, 1, 6)
    t = next(ts.trees())
    print(t.draw(format="unicode"))
    h = 200
    t.draw(path="wf-before.svg", width=200, height=h)
    tss, node_map = ts.simplify(map_nodes=True)
    node_labels = {
        node_map[j]: str(j) for j in range(node_map.shape[0])}
    t = next(tss.trees())
    # Rescale the height so that the nodes in the new tree are at the
    # same height as those in the old tree.
    h = h * 6 / 7
    print(t.draw(format="unicode", node_labels=node_labels))
    t.draw(path="wf-after.svg", node_labels=node_labels, width=200, height=h)
