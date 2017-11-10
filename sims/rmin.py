import msprime
import os
import libsequence.msprime
import libsequence.summstats

N = 2500.0
rate = 250.0

print('ftprime_S', 'ftprime_Rmin', 'msprime_S', 'msprime_Rmin')

for tf in [f for f in os.listdir() if f.find('tree_235569') == 0]:
    ft = msprime.load(tf)
    L = ft.sequence_length
    mt = msprime.simulate(50, recombination_rate=rate/(4.*N * L),
                          mutation_rate=rate/(4.*N * L), Ne=N, length=L)
    s = []
    for t in [ft, mt]:
        S = t.get_num_mutations()
        d = libsequence.msprime.make_SimData(t)
        ad = libsequence.summstats.PolySIM(d)
        minrec = ad.rm()
        s.append(S)
        s.append(minrec)
    print(*s)
