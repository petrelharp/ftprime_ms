#!/usr/bin/env python3.5
description = '''
Simulate a chromosome with scattered selected loci using simuPOP.
'''

import gzip
import sys
from argparse import ArgumentParser
import math
import time
import random

parser = ArgumentParser(description=description)
parser.add_argument("-T","--generations", dest="generations", type=int,
        help="number of generations to run for")
parser.add_argument("-N","--popsize", dest="popsize", type=int,
        help="size of the population", default=100)
parser.add_argument("-r","--recomb_rate", dest="recomb_rate", type=float,
        help="recombination rate", default=2.5e-8)
parser.add_argument("-L","--length", dest="chrom_length", type=int,
        help="number of bp in the chromosome", default=100)
parser.add_argument("-U","--neut_mut_rate", dest="neut_mut_rate", type=float,
        help="neutral mutation rate", default=1e-7)
parser.add_argument("-l","--nselloci", dest="nselloci", type=int,
        help="number of selected loci", default=20)
parser.add_argument("-u","--sel_mut_rate", dest="sel_mut_rate", type=float,
        help="mutation rate of selected alleles", default=1e-7)
parser.add_argument("-a","--gamma_alpha", dest="gamma_alpha", type=float,
        help="alpha parameter in gamma distributed selection coefficients", default=.23)
parser.add_argument("-b","--gamma_beta", dest="gamma_beta", type=float, 
        help="beta parameter in gamma distributed selection coefficients", default=5.34)
parser.add_argument("-k","--nsamples", dest="nsamples", type=int,
        help="number of *diploid* samples, total")
parser.add_argument("-o","--outfile", dest="outfile", type=str,
        help="name of output PED file (default: not output)", default=None)
parser.add_argument("-g","--logfile", dest="logfile", type=str,
        help="name of log file (or '-' for stdout)", default="-")
parser.add_argument("-s","--selloci_file", dest="selloci_file", type=str,
        help="name of file to output selected locus information", default="sel_loci.txt")
args = parser.parse_args()

if args.generations is None:
    parser.print_help()
    sys.exit()

if args.nsamples is None:
    args.nsamples = args.popsize

import simuOpt
simuOpt.setOptions(alleleType='mutant')
import simuPOP as sim
from simuPOP.utils import export
from simuPOP.sampling import drawRandomSample

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

if args.outfile is not None:
    outfile = fileopt(args.outfile, "w")
logfile = fileopt(args.logfile, "w")
selloci_file = args.selloci_file

logfile.write("Options:\n")
logfile.write(str(args)+"\n")
logfile.write(time.strftime('%X %x %Z')+"\n")
logfile.write("----------\n")
logfile.flush()

# locations of the loci along the chromosome?
rel_positions = [ random.expovariate(1) for k in range(args.chrom_length) ]
pos_fac = args.chrom_length/(sum(rel_positions) + random.expovariate(1))
locus_position = [x*pos_fac for x in rel_positions]

# which loci are under selection?
selected_loci = random.sample(range(1,args.chrom_length), args.nselloci)
neutral_loci = list(set(range(1,args.chrom_length)) - set(selected_loci))

# initially polymorphic alleles
init_freqs=[[k/100,1-k/100,0,0] for k in range(1,11)]
locus_classes=[min(len(init_freqs)-1,math.floor(random.expovariate(1))) for k in range(args.chrom_length)]
init_classes=[list(filter(lambda k: locus_classes[k]==x,range(args.chrom_length))) for x in range(len(init_freqs))]
init_geno=[sim.InitGenotype(freq=init_freqs[k],loci=init_classes[k]) for k in range(len(init_freqs))]

###
# random selection coefficients:
# modified from http://simupop.sourceforge.net/manual_svn/build/userGuide_ch5_sec9.html

class GammaDistributedFitness:
    def __init__(self, alpha, beta):
        # mean is alpha/beta
        self.coefMap = {}
        self.alpha = alpha
        self.beta = beta
    def __call__(self, loc, alleles):
        # because s is assigned for each locus, we need to make sure the
        # same s is used for fitness of genotypes 01 (1-s) and 11 (1-2s)
        # at each locus
        if loc in self.coefMap:
            s = self.coefMap[loc]
        else:
            s = random.gammavariate(self.alpha, self.beta)
            self.coefMap[loc] = s
        # print(str(loc)+":"+str(alleles)+"\n")
        # needn't return fitness for alleles=(0,0) as simupop knows that's 1
        if 0 in alleles:
            return 1. - s
        else:
            return 1. - 2.*s

pop = sim.Population(
        size=args.popsize,
        loci=[args.chrom_length],
        lociPos=locus_position,
        infoFields=['ind_id','fitness','migrate_to'])

pop.evolve(
    initOps=[
        sim.InitSex(),
    ]+init_geno,
    preOps=[
        sim.SNPMutator(u=args.neut_mut_rate,v=0,loci=neutral_loci),
        sim.SNPMutator(u=args.sel_mut_rate,v=0,loci=selected_loci),
        sim.PyMlSelector(GammaDistributedFitness(args.gamma_alpha, args.gamma_beta),
            loci=selected_loci, output=">>"+selloci_file),
    ],
    matingScheme=sim.RandomMating(
        ops=[
            sim.Recombinator(intensity=args.recomb_rate)
        ] ),
    postOps=[
        sim.Stat(numOfSegSites=sim.ALL_AVAIL, step=50),
        sim.PyEval(r"'Gen: %2d #seg sites: %d\n' % (gen, numOfSegSites)", step=50)
    ],
    gen = args.generations
)

logfile.write("Done simulating!\n")
logfile.write(time.strftime('%X %x %Z')+"\n")
logfile.write("----------\n")
logfile.flush()

sample = drawRandomSample(pop, sizes=args.nsamples)

if args.outfile is None:
    print("NOT writing out genotype data.\n")
else:
    print("Writing out genotype data to "+args.outfile+"\n")
    export(sample, format='PED', output=args.outfile)

logfile.write("Done writing out!\n")
logfile.write(time.strftime('%X %x %Z')+"\n")
logfile.write("----------\n")
logfile.flush()


logfile.write("All done!\n")
logfile.close()

