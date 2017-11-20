
# Script used to generate the data for the plot benchmarking simplify performance
# against the number of edges. This was copied from the fwdpy11_arg_example repository
# where it was originally in the update_to_edge branch.
import fwdpy11_arg_example.evolve_without_simplify
import numpy as np
import msprime
import time

before = time.process_time()
x = fwdpy11_arg_example.evolve_without_simplify.evolve(1000, 10000)
# x = fwdpy11_arg_example.evolve_without_simplify.evolve(100, 100)
duration = time.process_time() - before

print("Ran simulation in {} seconds".format(duration))

before = time.process_time()
sim_nodes = np.array(x.nodes, copy=False)
sim_edges = np.array(x.edges, copy=False)
nodes = msprime.NodeTable()
edges = msprime.EdgeTable()
flags = np.ones(len(sim_nodes), dtype=np.uint32)
nodes.set_columns(
    flags=flags, population=sim_nodes['population'], time=sim_nodes['generation'])
edges.set_columns(left=sim_edges['left'], right=sim_edges['right'],
                  parent=sim_edges['parent'], child=sim_edges['child'])
duration = time.process_time() - before

print("copies data into tables in {} seconds".format(duration))

msprime.sort_tables(nodes=nodes,edges=edges)
ts = msprime.load_tables(nodes=nodes, edges=edges)
ts.dump("tmp__NOBACKUP__/raw-simulation.hdf5")

