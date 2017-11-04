# coding: utf-8
import msprime
import random
from matplotlib import pyplot as plt

random.seed(111)
ts = msprime.load('tree.hdf5')
L = ts.sequence_length
NUM = 100

theta = 10.
rho = 10.
mut_rate = theta/4. / L
rec_rate = rho/4. / L
S_msprime = []

for _ in range(NUM):
    g = msprime.simulate(10, Ne=100, length=L, mutation_rate=mut_rate,
                         recombination_rate=rec_rate)
    S_msprime.append(len([i for i in g.variants()]))

rng = msprime.RandomGenerator(random.randint(1, 2**32 - 1))
nodes = msprime.NodeTable()
edges = msprime.EdgeTable()
sites = msprime.SiteTable()
mutations = msprime.MutationTable()
ts.dump_tables(nodes=nodes, edges=edges, sites=sites, mutations=mutations)

mutgen = msprime.MutationGenerator(rng, mut_rate)
mutgen.generate(nodes, edges, sites, mutations)
ts = msprime.load_tables(nodes=nodes, edges=edges, sites=sites,
                         mutations=mutations)

S_fwd = len([i for i in ts.variants()])

tmp = plt.hist(S_msprime, color='orange', normed=1)
plt.xlabel('Number variants')
plt.title(' '.join([str(NUM), 'msprime sim and 1 ftprime sim']))
plt.axvline(x=S_fwd)
plt.show()
