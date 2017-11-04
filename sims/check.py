# coding: utf-8
import msprime
import random
from matplotlib import pyplot as plt


random.seed(111)
ft_ts = msprime.load('simupoptree.hdf5')
L = ft_ts.sequence_length
fwd_ts = msprime.load('fwdpptree.hdf5')
L = ft_ts.sequence_length
#assert L == fwd_ts.sequence_length, "fwdpp {} and simupop {} don't match".format(fwd_ts.sequence_length, L)
NUM = 100

tss = {'simupop': ft_ts, 'fwdpp':  fwd_ts}

L = fwd_ts.sequence_length
theta = 10.
rho = 10.
mut_rate = theta/4./ L
rec_rate = rho/4. / L
S_msprime = []

for _ in range(NUM):
    g = msprime.simulate(10, Ne=100, length=L, mutation_rate=mut_rate,
                         recombination_rate=rec_rate)
    S_msprime.append(len([i for i in g.variants()]))

k ='fwdpp'
ts = fwd_ts

# for k, ts in tss.items():
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
tss[k] = ts





tmp = plt.hist(S_msprime, color='orange', normed=1)
plt.xlabel('Number variants')
plt.title(' '.join([str(NUM), 'msprime sim and 1', 'fwdpp', 'sim']))
#for k, ts in tss.items():
plt.axvline(x=len([i for i in ts.variants()]))
plt.savefig('check-results.png')
