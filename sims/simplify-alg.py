"""
Python implementation of Algorithm S.

The example works by generating an initial TreeSequence
for a sample of 10 haplotypes using msprime.  We then
simplify the node/edge table in that TreeSequence with
respect to the first three samples.

Requires msprime >= 0.6.0
"""
import heapq
import numpy as np

import msprime


class Segment(object):
    """
    An ancestral segment mapping a given node ID to a half-open genomic
    interval [left, right).
    """
    def __init__(self, left, right, node):
        assert left < right
        self.left = left
        self.right = right
        self.node = node

    def __lt__(self, other):
        # We implement the < operator so that we can use the heapq directly.
        # We are only interested in the left coordinate.
        return self.left < other.left

    def __repr__(self):
        return repr((self.left, self.right, self.node))


def simplify(S, Ni, Ei, L):
    """
    This is an implementation of the simplify algorithm described in Appendix A
    of the paper.
    """
    tables = msprime.TableCollection(L)
    No = tables.nodes
    Eo = tables.edges
    A = [[] for _ in range(len(Ni))]
    Q = []

    for u in S:
        v = No.add_row(time=Ni.time[u], flags=1)
        A[u] = [Segment(0, L, v)]

    for u in range(len(Ni)):
        for e in [e for e in Ei if e.parent == u]:
            for x in A[e.child]:
                if x.right > e.left and e.right > x.left:
                    y = Segment(max(x.left, e.left), min(x.right, e.right), x.node)
                    heapq.heappush(Q, y)
        v = -1
        while len(Q) > 0:
            l = Q[0].left
            r = L
            X = []
            while len(Q) > 0 and Q[0].left == l:
                x = heapq.heappop(Q)
                X.append(x)
                r = min(r, x.right)
            if len(Q) > 0:
                r = min(r, Q[0].left)

            if len(X) == 1:
                x = X[0]
                alpha = x
                if len(Q) > 0 and Q[0].left < x.right:
                    alpha = Segment(x.left, Q[0].left, x.node)
                    x.left = Q[0].left
                    heapq.heappush(Q, x)
            else:
                if v == -1:
                    v = No.add_row(time=Ni.time[u])
                alpha = Segment(l, r, v)
                for x in X:
                    Eo.add_row(l, r, v, x.node)
                    if x.right > r:
                        x.left = r
                        heapq.heappush(Q, x)

            A[u].append(alpha)

    # Sort the output edges and compact them as much as possible into
    # the output table. We skip this for the algorithm listing as it's pretty mundane.
    # Note: could be replaced with calls to squash_edges() and sort_tables()
    E = list(Eo)
    Eo.clear()
    E.sort(key=lambda e: (e.parent, e.child, e.right, e.left))
    start = 0
    for j in range(1, len(E)):
        condition = (
            E[j - 1].right != E[j].left or
            E[j - 1].parent != E[j].parent or
            E[j - 1].child != E[j].child)
        if condition:
            Eo.add_row(E[start].left, E[j - 1].right, E[j - 1].parent, E[j - 1].child)
            start = j
    j = len(E)
    Eo.add_row(E[start].left, E[j - 1].right, E[j - 1].parent, E[j - 1].child)

    return tables.tree_sequence()



def verify():
    """
    Checks that simplify() does the right thing, by comparing to the implementation
    in msprime.
    """
    for n in [10, 100, 1000]:
        ts = msprime.simulate(n, recombination_rate=1, random_seed=1)
        nodes = ts.tables.nodes
        edges = ts.tables.edges
        print("simulated for ", n)

        for N in range(2, 10):
            sample = list(range(N))
            ts1 = simplify(sample, nodes, edges, ts.sequence_length)
            ts2 = ts.simplify(sample)

            n1 = ts1.tables.nodes
            n2 = ts2.tables.nodes
            assert np.array_equal(n1.time, n2.time)
            assert np.array_equal(n1.flags, n2.flags)
            e1 = ts1.tables.edges
            e2 = ts2.tables.edges
            assert np.array_equal(e1.left, e2.left)
            assert np.array_equal(e1.right, e2.right)
            assert np.array_equal(e1.parent, e1.parent)
            assert np.array_equal(e1.child, e1.child)


if __name__ == "__main__":
    # verify()

    # Generate initial TreeSequence
    ts = msprime.simulate(10, recombination_rate=2, random_seed=1)
    nodes = ts.tables.nodes
    edges = ts.tables.edges

    # Simplify nodes and edges with respect to the following samples:
    sample = [0, 1, 2]
    ts1 = simplify(sample, nodes, edges, ts.sequence_length)
    print(ts1.tables)
