"""
Set-theoretic algorithm implementation of Algorithm S.

The example works by generating an initial TreeSequence
for a sample of 10 haplotypes using msprime.  We then
simplify the node/edge table in that TreeSequence with
respect to the first three samples.
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
    A = [intervaltree.IntervalTree() for _ in range(len(Ni))]
    for input_id in S:
        # TODO update node table to return ID of new row.
        output_id = len(No)
        No.add_row(time=time[input_id], flags=1)
        A[output_id] = intervaltree.IntervalTree([intervaltree.Interval(0, L, input_id)])

    E = []
    for input_parent in range(len(Ni)):
        index = parent == input_parent
        new_output_id = -1
        P = intervaltree.IntervalTree()
        for l, r, c in zip(left[index], right[index], child[index]):
            # We have to slice the intervals to make sure we only return the bits
            # we're interested in.
            A[c].slice(l)
            A[c].slice(r)
            # Note there's no need to actually remove the ancestral material. We just
            # leave it in there because it can't affect anything later.
            P = P.union(A[c][l: r])
        P.split_overlaps()
        for l, r, output_id in  P:
            # We look at each distinct segment in turn. If there are coalescences, there
            # will be segments that overlap each other which we detect by the effects
            # on A[input_parent]
            A[input_parent].slice(l)
            A[input_parent].slice(r)
            if len(A[input_parent][l: r]) == 0:
                A[input_parent][l: r] = output_id
            else:
                if new_output_id == -1:
                    new_output_id = len(No)
                    No.add_row(time=time[input_parent], flags=0)
                child_output_id = list(A[input_parent][l:r])[0].data
                if child_output_id != new_output_id:
                    E.append(Edge(l, r, new_output_id, child_output_id))
                E.append(Edge(l, r, new_output_id, output_id))
                A[input_parent].remove_overlap(l, r)
                A[input_parent][l: r] = new_output_id

    # Sort the output locus-wise edges and compact them as much as possible into
    # the output table. We can probably skip this for the algorithm listing as
    # it's pretty mundane.
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
            # For each locus, pull out any genetic material and transfer to the parent.
            P = np.zeros(L, dtype=int) - 1
            P[l: r] = A[c, l: r]
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
        ts = msprime.simulate(n, recombination_rate=1, random_seed=1)
        nodes= ts.tables.nodes
        edges = ts.tables.edges
        print("simulated for ", n)

        # # convert left and right to breakpoints
        # breakpoints = np.unique(np.hstack([edges.left, edges.right]))
        # breakpoint_map = dict(zip(breakpoints, range(breakpoints.shape[0])))
        # # Build a new edge table
        # edges = msprime.EdgeTable()
        # for e in ts.edges():
        #     edges.add_row(
        #         breakpoint_map[e.left], breakpoint_map[e.right], e.parent, e.child)

        for N in range(2, 10):
            sample = list(range(N))

            # ts1 = simplify_loci(sample, nodes, edges, len(breakpoint_map) - 1)
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
            # assert np.array_equal(breakpoints[e1.left.astype(int)], e2.left)
            # assert np.array_equal(breakpoints[e1.right.astype(int)], e2.right)
            assert np.array_equal(e1.parent, e1.parent)
            assert np.array_equal(e1.child, e1.child)

if __name__ == "__main__":
    verify()

    # Generate initial TreeSequence
    ts = msprime.simulate(10, recombination_rate=2, random_seed=1)
    nodes= ts.tables.nodes
    edges = ts.tables.edges

    # convert left and right to breakpoints
    # breakpoints = np.unique(np.hstack([edges.left, edges.right]))
    # breakpoint_map = dict(zip(breakpoints, range(breakpoints.shape[0])))
    # Build a new edge table
    # edges = msprime.EdgeTable()
    # for e in ts.edges():
    #     edges.add_row(
    #         breakpoint_map[e.left], breakpoint_map[e.right], e.parent, e.child)

    # Simplify nodes, edges 
    # with respect to
    # the following samples:
    sample = [0, 1, 2]
    ts1 = simplify(sample, nodes, edges, ts.sequence_length)
    # ts1 = simplify_loci(sample, nodes, edges, len(breakpoint_map) - 1)

    print(ts1.tables)



