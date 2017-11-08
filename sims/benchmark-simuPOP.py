#!/usr/bin/env python3
import gzip
import sys
import time
import random
from ftprime import RecombCollector
import msprime
import argparse
import pandas as pd

description = '''
Benchmark

Desired interface:

parallel --timeout 2 python benchmark-simuPOP.py -N 1000 --theta 100 --rho 100 \
    --pdel 0.1 --nsam 10 --gc 100 --seed ::: 42
'''
# Notes from K Thornton / P Ralph discussion (summary by KT):
# 1. Fitness at a single site for the genotypes AA, AA, and aa
# 1, 1+sh, 1+s.
# **I vote for h = 0.5.

# X2. How to calculate fitness across sites.
# ** I vote for multiplicative.

# X 3. The DFE itself.
# I think we decided that the DFE will be on 2Ns rather than on s.
# ** I vote for (-1.0)*Gamma(shape=1.0,scale=5.0).  This gives us a mean |2Ns|
# of 5 and 30% of new mutations have 2 <= |2Ns| <= 5, which is an interesting
# domain where deleterious variants can persists for some time.

# X 4. Mutation and recombination rates.
# These are scaled as 4Nu and 4Nr, respectively.  We also decided 4Nu = 4Nr.
# ** I propose 4Nu \in {1e3, 1e4, 1e5}, which is roughly 1, 10, and 100Mb of a
# "human" chromosome.
# ** I propose that rates are uniform along the regions.

# X 5. Population size.
# ** I propose N \in {1e3, 1e4, 1e5}

# X 6. Simulation length
# ** 20N generations.  We kinda need this until Jerome addresses the issues
# w/incompletely-coalesced marginal trees.

# X (solved in submission script) 7. The max run time.
# ** I propose 72 hours.  In the past, I've done one week, but my preliminary
# results suggest I can do N=1e4, 4Nu=4Nr=1e5 in just a few hours (!!!!!).  I
# fully expect sims including all neutral variants to hit this max time for when
# N and/or 4Nu/r are large.

# X 8. The rate at which deleterious mutations arise.
# ** I propose we keep this as a constant function of 4Nu.  For no particular
# reason, let's say 0.1.  Thus, for a given \theta = 4Nu, the rate at which
# deleterious variants arise will be 0.1u.  As we increase 4Nu/r, we are
# simulating a bigger and bigger region, holding the fraction of deleterious new
# mutations constant means modeling "the same, but bigger."

# Increasing 4Nr = increasing the region size.  Varying N holding f(2Ns)
# constant keeps the expected number of variants in a sample constant for a
# given (4Nu,4Nr) tuple.  Varying N but keeping the # generations simulated
# allows us to report (total run time)/(20N) to get mean time spent in a
# generation.
#
# For simuPOP: theta = 4N(u/site)*L, where L is the
# number is sites, and u/site is held constant.  Likewise for 4Nr.
REPORTING_STEP = 100


def fileopt(fname,opts):
    '''Return the file referred to by fname, open with options opts;
    if fname is "-" return stdin/stdout; if fname ends with .gz run it through gzip.
    '''
    if fname == "-":
        if opts == "r":
            fobj = sys.stdin
        elif opts == "w":
            fobj = sys.stdout
        else:
            print("Something not right here.")
    elif fname[len(fname)-3:len(fname)]==".gz":
        fobj = gzip.open(fname,opts)
    else:
        fobj = open(fname,opts)
    return fobj

parser = argparse.ArgumentParser(description=description)
parser.add_argument("--popsize","-N", type=int, dest="popsize",
        help="size of each subpopulation",default=100)
parser.add_argument("--theta","-ϴ", type=int, dest="theta",
                    help="total mutation rate for whole chromosome: theta = 4 N u/site (sites)", default=100)
parser.add_argument("--rho","-ρ", type=int, dest="rho",
                    help="total recombination rate for whole chromosome: rho = 4 N r/site (sites)", default=100)
parser.add_argument("--nsam","-k", type=int, dest="nsamples",
        help="number of *diploid* samples, total",)
parser.add_argument("--pdel","-p", type=float, dest="pdel",
        help="Ratio of deleterious mutations to neutral mutations",)
parser.add_argument("--record-neutral", type=bool, dest="record_neutral",
                    default=False)

parser.add_argument("--gamma_shape","-a", type=float, dest="gamma_shape",
        help="shape parameter in gamma distributed selection coefficients",
                    default=1.0)
parser.add_argument("--gamma_scale","-b", type=float, dest="gamma_scale",
        help="scale parameter in gamma distributed selection coefficients",
                    default=5.00)
parser.add_argument("--gc", "-G", dest="simplify_interval", type=int,
        help="Interval between simplify steps.", default=500)
parser.add_argument("--logfile","-g", type=str, dest="logfile",
        help="name of log file (or '-' for stdout)",default="/dev/null")
parser.add_argument("--outfile1","-o", type=str, dest="outfile1",
        help="name of csv file to write timing statisitcs.")
parser.add_argument("--seed", "-d", dest="seed", type=int, help="random seed")

# optional args
parser.add_argument("--recomb_rate","-r", type=float, dest="recomb_rate",
        help="recombination rate",default=1e-7) # was 2.5e-8 but pin to mut rate
parser.add_argument("--mut_rate","-U", type=float, dest="mut_rate",
        help="mutation rate of neutral alleles", default=1e-7)
parser.add_argument("--treefile","-t", type=str, dest="treefile",
        help="name of output file for trees (default: not output)",default=None)
parser.add_argument("--generations","-T", type=int, dest="generations",
        help="number of generations to run for (default SIMLEN * N)",
                    default=None)
parser.add_argument("--simlen","-s", type=int, dest="multiplier",
        help="multiplier of popsize to run for (unless `generations` is specified)",
                    default=10)
parser.add_argument("--verbose", "-v", dest="verbose", action='store_true')
parser.add_argument("--num-vars", "-n", dest="num_vars", action='store_true',
                    help="print the number of variants post mut")


args = parser.parse_args()
if args.record_neutral:
    sys.exit(1)

if args.generations is None:
    args.generations = args.popsize * args.multiplier

from simuOpt import setOptions
setOptions(alleleType = 'mutant')
setOptions(optimized=True)
if not args.verbose:
    setOptions(quiet=True)


import simuPOP as sim

sim.setRNG(seed=args.seed)
random.seed(args.seed)

logfile = fileopt(args.logfile, "w")

logfile.write("Options:\n")
logfile.write(str(args)+"\n")
logfile.write(time.strftime('%X %x %Z')+"\n")
logfile.write("----------\n")
logfile.flush()

# define defaults for benchmark
# scalings:
# theta = 4 * Ne * mutation rate per bp * total number of bp
# rho = 4 * Ne * mutation rate per bp * total number of bp
npops = 1
rloci = args.rho / (args.popsize * 4 * args.recomb_rate)
uloci = args.theta / (args.popsize * 4 * args.mut_rate)
assert rloci == uloci
args.nloci = int(rloci)
args.sel_mut_rate = args.mut_rate * args.pdel

# hard code defaults for simupop:
# >The default positions are 1, 2, 3, 4, ... on each
# >chromosome.

locus_position = list(i / args.nloci for i in range(0, args.nloci))

# logfile.write("Locus positions:\n")
# logfile.write(str(locus_position)+"\n")
# logfile.write("----------\n")
# logfile.flush()

###
# modified from http://simupop.sourceforge.net/manual_svn/build/userGuide_ch5_sec9.html

class GammaDistributedFitness:
    def __init__(self, shape, scale, popsize):
        # mean is shape/scale
        self.coefMap = {}
        # these are called alpha/beta by `random.gammavariate` but are
        # implemented as shape/scale paramterization
        #
        self.alpha = shape
        self.beta = scale
        self.two_N = popsize * 2.

    def __call__(self, loc, alleles):
        # because s is assigned for each locus, we need to make sure the
        # same s is used for fitness of genotypes 01 (1-s) and 11 (1-2s)
        # at each locus
        if loc in self.coefMap:
            s = self.coefMap[loc]
        else:
            s = random.gammavariate(self.alpha, self.beta)
            self.coefMap[loc] = s / self.two_N
        # print(str(loc)+":"+str(alleles)+"\n")
        # simupop does not call function for alleles=(0,0)
        if 0 in alleles:
            return max(0.0, 1. - s / 2.)
        else:
            return max(0.0, 1. - s)

before_time = time.process_time()

init_geno=[sim.InitGenotype(freq=1.0)]

pop = sim.Population(
        size=[args.popsize]*npops, 
        loci=[args.nloci], 
        lociPos=locus_position,
        infoFields=['ind_id', 'fitness'])

id_tagger = sim.IdTagger()
id_tagger.apply(pop)

# set up recomb collector
# NB: we have to simulate an initial tree sequence
first_gen = pop.indInfo("ind_id")
init_ts = msprime.simulate(2*len(first_gen),
                           Ne=args.popsize,
                           recombination_rate=args.recomb_rate,
                           length=max(locus_position))
haploid_labels = [(k,p) for k in first_gen
                        for p in (0,1)]
node_ids = {x:j for x, j in zip(haploid_labels, init_ts.samples())}
rc = RecombCollector(ts=init_ts, node_ids=node_ids,
                     locus_position=locus_position,
                     benchmark=True)

pop.evolve(
    initOps=[
        sim.InitSex(),
    ]+init_geno,
    preOps=[
        sim.PyOperator(lambda pop: rc.increment_time() or True),
        sim.SNPMutator(u=args.sel_mut_rate, v=args.sel_mut_rate),
        # so that selector returns, for f_i fitness values, \prod_i f_i
        sim.PyMlSelector(GammaDistributedFitness(shape=args.gamma_shape,
                                                 scale=args.gamma_scale,
                                                 popsize=args.popsize),
                         mode=sim.MULTIPLICATIVE),
    ],
    matingScheme=sim.RandomMating(
        ops=[
            id_tagger,
            sim.Recombinator(rates=args.recomb_rate, output=rc.collect_recombs,
                             infoFields="ind_id"),
        ] ),
    postOps=[
        sim.PyOperator(lambda pop: rc.simplify(pop.indInfo("ind_id")) or True,
                       step=args.simplify_interval),
    ],
    gen = args.generations
)

tsim = time.process_time()- before_time

logfile.write("Done simulating!\n")
logfile.write(time.strftime('%X %x %Z')+"\n")
logfile.write("----------\n")
logfile.flush()

logfile.write("Collecting samples:\n")
logfile.write("  " + str(args.nsamples) + " of them")
logfile.write("  " + "ids:" + str(pop.indInfo("ind_id")))

diploid_samples = random.sample(pop.indInfo("ind_id"), args.nsamples)
rc.simplify(diploid_samples)

del pop

logfile.write("Samples:\n")
logfile.write(str(rc.diploid_samples)+"\n")
logfile.write("----------\n")
logfile.flush()

ts = rc.args.tree_sequence()

times = rc.args.timings.times
args.gc = args.simplify_interval  # so use same name below

## begin block similar to K Thornton's
# Take times from args before they change.
times['total_runtime'] = [tsim]
times['N'] = [args.popsize]
times['theta'] = [args.theta]
times['rho'] = [args.rho]
times['simplify_interval'] = [args.gc]
d = pd.DataFrame(times)
d.to_csv(args.outfile1,sep='\t',index=False,compression='gzip')

del rc

logfile.write("Loaded into tree sequence!\n")
logfile.write(time.strftime('%X %x %Z')+"\n")
logfile.write("----------\n")
logfile.flush()

if args.treefile is not None:
    ts.dump(args.treefile)

logfile.write("Writing out samples.\n")
logfile.write(time.strftime('%X %x %Z')+"\n")
logfile.write("----------\n")
logfile.flush()

mut_seed=args.seed
logfile.write(time.strftime('%X %x %Z')+"\n")
logfile.write("Generating mutations with seed "+str(mut_seed)+"\n")
logfile.flush()

rng = msprime.RandomGenerator(mut_seed)
nodes = msprime.NodeTable()
edges = msprime.EdgeTable()
sites = msprime.SiteTable()
ts.dump_tables(nodes=nodes, edges=edges)
if args.record_neutral:
    mutated_ts = msprime.load_tables(nodes=nodes, edges=edges,
                                     sites=sites)
elif not args.record_neutral:
    mutations = msprime.MutationTable()
    mutgen = msprime.MutationGenerator(rng, args.mut_rate)
    mutgen.generate(nodes, edges, sites, mutations)
    mutated_ts = msprime.load_tables(
        nodes=nodes, edges=edges, sites=sites, mutations=mutations)
if args.num_vars:
    print(len([i for i in mutated_ts.variants()]))
del ts

logfile.write("Generated mutations!\n")
logfile.write(time.strftime('%X %x %Z')+"\n")
logfile.write("Mean pairwise diversity: {}\n".format(mutated_ts.get_pairwise_diversity()/mutated_ts.get_sequence_length()))
logfile.write("Sequence length: {}\n".format(mutated_ts.get_sequence_length()))
logfile.write("Number of trees: {}\n".format(mutated_ts.get_num_trees()))
logfile.write("Number of mutations: {}\n".format(mutated_ts.get_num_mutations()))

logfile.write("All done!\n")
logfile.close()
