"""
Set-theoretic algorithm implementation of Algorithm S.
"""
import collections
import msprime
import numpy as np

def simplify(S, Ni, Ei, L):
    No = msprime.NodeTable()
    Eo = msprime.EdgeTable()
    left = Ei.left.astype(int)
    right = Ei.right.astype(int)
    child = Ei.child
    parent = Ei.parent
    time = Ni.time
    A = collections.defaultdict(set)
    M = {}
    for input_id in S:
        # TODO update node table to return ID of new row.
        output_id = len(No)
        No.add_row(time=time[input_id])
        M[input_id] = output_id
        # TODO We probably need to make this a set of tuples, otherwise we lose the
        # ability to track where individual bits have come from.
        A[output_id] = set(range(L - 1))
    for k, v in A.items():
        print(k, "->", v)

    # This isn't quite right as we've lost the ability to map nodes. Seems like
    # it's OK otherwise.

    for input_parent in range(len(Ni)):
        index = parent == input_parent
        print("parent = ", input_parent)
        S = []
        for l, r, c in zip(left[index], right[index], child[index]):
            # Remove ancestry is now trivial; directly expressed as set operations.
            x = set(range(l, r))
            S.append(A[c] & x)
            A[c] -= x
        if len(S) > 0:
            print("S = ", S)
            A[input_parent] = S[0].union(*S[1:])
            for k, v in A.items():
                if len(v) > 0:
                    print(k, "->", v)
            inter = S[0].intersection(*S[1:])
            if len(inter) > 0:
                # Allocate a new node
                output_parent = len(No)
                No.add_row(time=time[input_parent])
                M[input_parent] = output_parent

                # Figure out which intervals they are children over.
                for l, r, c in zip(left[index], right[index], child[index]):
                    x = set(range(l, r))
                    child_inter = x & inter
                    if len(child_inter) > 0:
                        # And we record the outptu edge
                        print("EDGE {} {} over {}".format(c, input_parent, child_inter))







if __name__ == "__main__":
    # ts = msprime.simulate(10, recombination_rate=2, random_seed=1)
    # ts.dump("example.ts")
    # ts = msprime.simulate(10, recombination_rate=2, random_seed=1)
    # ts.dump("example.ts")
    ts = msprime.load("example.ts")
    nodes= ts.tables.nodes
    edges = ts.tables.edges
    # convert left and right to breakpoints
    breakpoints = np.unique(np.hstack([edges.left, edges.right]))
    breakpoint_map = dict(zip(breakpoints, range(breakpoints.shape[0])))
    # Build a new edge table
    edges = msprime.EdgeTable()
    for e in ts.edges():
        edges.add_row(
            breakpoint_map[e.left], breakpoint_map[e.right], e.parent, e.child)

    ts_new = simplify([0, 1, 2], nodes, edges, len(breakpoint_map))
