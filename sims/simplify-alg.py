"""
Set-theoretic algorithm implementation of Algorithm S.
"""
import numpy as np

import msprime
import intervaltree

def simplify(S, Ni, Ei, L):
    No = msprime.NodeTable()
    Eo = msprime.EdgeTable()
    left = Ei.left
    right = Ei.right
    child = Ei.child
    parent = Ei.parent
    time = Ni.time
    # TODO Should be an interval tree for each ID.
    A = {}
    for input_id in S:
        # TODO update node table to return ID of new row.
        output_id = len(No)
        No.add_row(time=time[input_id], flags=1)
        A[output_id] = intervaltree.IntervalTree([
            intervaltree.Interval(0, L, input_id)])
    print(A)

    for input_parent in range(len(Ni)):
        index = parent == input_parent
        output_id = -1
        S = []
        for l, r, c in zip(left[index], right[index], child[index]):
            # TODO Snip out this part of the interval tree for c, and save it in a
            # list of intervals.
            if c in A:
                P = A[c][l: r]
                print(P)

            # # For each locus, transfer any genetic material to the parent.
            # P = np.zeros(L, dtype=int) - 1
            # P[l: r] = A[c, l: r]
            # A[c, l: r] = -1
            # # Store the transferred genetic material for all parents in the
            # # list S so that we can find any coalescences afterwards.
            # S.append(P)




class Edge(object):
    def __init__(self, left, right, parent, child):
        self.left = left
        self.right = right
        self.parent= parent
        self.child = child

    def __repr__(self):
        return repr([self.left, self.right, self.parent, self.child])



def simplify_loci(S, Ni, Ei, L):
    No = msprime.NodeTable()
    Eo = msprime.EdgeTable()
    left = Ei.left.astype(int)
    right = Ei.right.astype(int)
    child = Ei.child
    parent = Ei.parent
    time = Ni.time
    A = np.zeros((len(Ni), L), dtype=int) - 1
    M = np.zeros(len(Ni), dtype=int) - 1
    for input_id in S:
        # TODO update node table to return ID of new row.
        output_id = len(No)
        No.add_row(time=time[input_id], flags=1)
        A[output_id, :] = input_id

    E = []

    for input_parent in range(len(Ni)):
        index = parent == input_parent
        output_id = -1
        S = []
        for l, r, c in zip(left[index], right[index], child[index]):
            # For each locus, transfer any genetic material to the parent.
            P = np.zeros(L, dtype=int) - 1
            P[l: r] = A[c, l: r]
            A[c, l: r] = -1
            # Store the transferred genetic material for all parents in the
            # list S so that we can find any coalescences afterwards.
            S.append(P)
        if len(S) > 0:
            S = np.array(S)
            for k in range(L):
                # For each locus k, see if we have any ancestral material present.
                cond = np.where(S[:, k] >= 0)[0]
                if cond.shape[0] == 1:
                    # If we have only one edge with ancestral material at this locus
                    # then we transfer it directly to the parent.
                    A[input_parent, k] = S[cond[0], k]
                elif cond.shape[0] > 1:
                    # If more than one edge has ancestral material at this locus then
                    # we have a coalescence, which we must record.
                    if output_id == -1:
                        output_id = len(No)
                        No.add_row(time=time[input_parent], flags=0)
                    A[input_parent, k] = output_id
                    for c in S[cond, k]:
                        E.append(Edge(k, k + 1, output_id, c))

    # Sort the output locus-wise edges and compact them as much as possible into
    # the output table.
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
    return msprime.load_tables(nodes=No, edges=Eo)



def verify():
    for n in [10, 100, 1000]:
        ts = msprime.simulate(n, recombination_rate=5, random_seed=1)
        nodes= ts.tables.nodes
        edges = ts.tables.edges
        print("simulated for ", n)

        # convert left and right to breakpoints
        breakpoints = np.unique(np.hstack([edges.left, edges.right]))
        breakpoint_map = dict(zip(breakpoints, range(breakpoints.shape[0])))
        # Build a new edge table
        edges = msprime.EdgeTable()
        for e in ts.edges():
            edges.add_row(
                breakpoint_map[e.left], breakpoint_map[e.right], e.parent, e.child)

        for N in range(2, 10):
            sample = list(range(N))

            ts1 = simplify(sample, nodes, edges, len(breakpoint_map) - 1)
            ts2 = ts.simplify(sample)

            n1 = ts1.tables.nodes
            n2 = ts2.tables.nodes
            assert np.array_equal(n1.time, n2.time)
            assert np.array_equal(n1.flags, n2.flags)
            e1 = ts1.tables.edges
            e2 = ts2.tables.edges
            assert np.array_equal(breakpoints[e1.left.astype(int)], e2.left)
            assert np.array_equal(breakpoints[e1.right.astype(int)], e2.right)
            assert np.array_equal(e1.parent, e1.parent)
            assert np.array_equal(e1.child, e1.child)

if __name__ == "__main__":
    # verify()

    ts = msprime.simulate(10, recombination_rate=2, random_seed=1)
    nodes= ts.tables.nodes
    edges = ts.tables.edges

#     # convert left and right to breakpoints
#     breakpoints = np.unique(np.hstack([edges.left, edges.right]))
#     breakpoint_map = dict(zip(breakpoints, range(breakpoints.shape[0])))
#     # Build a new edge table
#     edges = msprime.EdgeTable()
#     for e in ts.edges():
#         edges.add_row(
#             breakpoint_map[e.left], breakpoint_map[e.right], e.parent, e.child)

    sample = [0, 1, 2]
    ts1 = simplify(sample, nodes, edges, ts.sequence_length)

    print(ts1.tables)



