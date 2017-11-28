import os, sys, timeit, time


def memory(N, theta):
    loci = theta / (N * 4 * 1e-7)
    ploidy=2
    # Number of generation
    gen = N * 10
    # Memory Size (GB)
    memsize = 8
    # both 'short' and 'mutant' have 256 maximum allelic states so maybe same
    # memory use?  but actually the whole point of mutatnt is to use less memory
    # so... unclear what to do here
    if alleleType == 'short' or 'mutant':
        size = (memsize * 1024.0 * 1024.0 * 1024.0) / ((loci*ploidy*1.0 + 24.0)*2.0 + 8)
    elif alleleType == 'long':
        size = (memsize * 1024.0 * 1024.0 * 1024.0) / ((loci*ploidy*4.0 + 24.0)*2.0 + 8)
    elif alleleType == 'binary':
        size = (memsize * 1024.0 * 1024.0 * 1024.0) / ((loci*ploidy/8.0 + 32.0)*2.0 + 8)
    mating = timeit.Timer(
        setup = 'from __main__ import Population, InitSex, RandomMating,'
            'MendelianGenoTransmitter\n'
            "pop = Population(size=%d, loci=%d, ploidy = %d)" % (size, loci, ploidy),
        stmt = "pop.evolve(\n"
            "initOps=InitSex(),\n"
            "matingScheme=RandomMating(ops=MendelianGenoTransmitter()),\n"
            "gen=%d)" % gen)
    print(">Maximum number of population size: %d\n>Time(sec):%f" % (size,
        mating.timeit(number=1)))

if __name__ == '__main__':
    # Number of processors(CPU Core)
    numThreads=1
    alleleType='mutant'
    from simuOpt import setOptions
    setOptions(quiet=True)
    setOptions(alleleType = alleleType)
    setOptions(numThreads = numThreads)
    from simuPOP import *
    print("How many individuals can we simulate in 8GB of ram for")
    for N, theta in [(1000, 1000), (1000, 5000), (1000, 10000),
                     (5000, 1000), (5000, 5000)]:
        print("T =" , 10 * N, " generations; theta =", theta, "?")
        memory(N, theta)


