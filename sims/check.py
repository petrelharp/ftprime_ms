# coding: utf-8
import msprime
import random
import argparse
from matplotlib import pyplot as plt


parser = argparse.ArgumentParser(description='small test script')
parser.add_argument("--popsize","-N", type=int, dest="popsize",
        help="size of each subpopulation",default=100)
parser.add_argument("--theta","-ϴ", type=int, dest="theta",
                    help="total mutation rate for whole chromosome: theta = 4 N u/site (sites)", default=100)
parser.add_argument("--rho","-ρ", type=int, dest="rho",
                    help="total **diploid** recombination rate for whole chromosome: rho = 4 N r/site (sites)", default=100)
parser.add_argument("--nsam","-k", type=int, dest="nsam",
                    help="total number of samples with msprime", default=10)
parser.add_argument("--sims","-n", type=int, dest="NUM",
                    help="total number of sims with msprime", default=100)
parser.add_argument("--seed","-s", type=int, dest="seed",
                    help="random seed")
parser.add_argument("--out-fig","-o", type=str, dest="figname",
                    help="desination, e.g. check-results.png")
args = parser.parse_args()

random.seed(args.seed)
ft_ts = msprime.load('simupoptree.hdf5')
L = ft_ts.sequence_length

L = ft_ts.sequence_length
theta = args.theta
rho = args.rho
Ne = args.popsize
mut_rate = theta/4./ L /Ne
rec_rate = rho/4. / L /Ne
S_msprime = []

for _ in range(args.NUM):
    g = msprime.simulate(2 * args.nsam, Ne=Ne, length=L, mutation_rate=mut_rate,
                         recombination_rate=rec_rate / 2.0)
    S_msprime.append(len([i for i in g.variants()]))

rng = msprime.RandomGenerator(random.randint(1, 2**32 - 1))
nodes = msprime.NodeTable()
edges = msprime.EdgeTable()
sites = msprime.SiteTable()
mutations = msprime.MutationTable()
ft_ts.dump_tables(nodes=nodes, edges=edges, sites=sites, mutations=mutations)
mutgen = msprime.MutationGenerator(rng, mut_rate)
mutgen.generate(nodes, edges, sites, mutations)
ft_ts = msprime.load_tables(nodes=nodes, edges=edges, sites=sites,
                         mutations=mutations)



tmp = plt.hist(S_msprime, color='orange', normed=1)
plt.xlabel('Number variants')
plt.title(' '.join([str(args.NUM), 'msprime sim and 1', 'ftprime', 'sim']))
#for k, ts in tss.items():
plt.axvline(x=len([i for i in ft_ts.variants()]))
plt.savefig(args.figname)
