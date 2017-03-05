This uses:

- [ftprime](https://github.com/ashander/ftprime)
- [msprime](https://github.com/petrelharp/msprime/tree/has_mutations) before refactoring: commit 8a894a99b42bb3a58e85fe7cbf7200e3cc9bd595
- [simuPOP](https://github.com/BoPeng/simuPOP)

Proposed default simulation parameters:

- randomly mating population of size 1,000
- for 4,000 generations, with a common ancestor 1,000 generations before this
- recombination rate 1e-7 per generation per base pair
- mutation rate 1e-7 per generation per base pair
- selected locus every 1Kb with gamma(alpha=.23,beta=5.34)-distributed selection coefficient (mean s=.043)
- 100 sampled diploid genomes
- locus of 1,000 bp

This is small/short, but we need to start from something easy
and build up from here.

Then we can collect timing and memory usage for

- locus length increases to 100 Mb: 1 Kb / 10 Kb / 100 Kb / 1 Mb / 10 Mb / 100 Mb
- other parameters? or stick to this?

To do this (short, test version:)
```sh

N=10
T=40
A=10
recomb="1e-7"
mut="1e-7"
nsamp=10
L=1000
nsel=$((1 + $L / 1000))
JOBID=$RANDOM

OUTDIR="sim_N_${N}_T_${T}_A_${A}_recomb_${recomb}_mut_${mut}_nsamp_${nsamp}_L_${L}_nsel_${nsel}_run_$JOBID"
mkdir -p $OUTDIR

/usr/bin/time --format="elapsed: %E / kernel: %S / user: %U / mem: %M" \
    ./run-sim.py -T $T -N $N -A $A -r $recomb -u $mut -U $mut -k $nsamp -L $L -l $nsel \
    -g $OUTDIR/run-sim.log -o $OUTDIR/run-sim.vcf -s $OUTDIR/run-sim.selloci.txt -t $OUTDIR/run-sim.trees &> $OUTDIR/run-sim.time

/usr/bin/time --format="elapsed: %E / kernel: %S / user: %U / mem: %M" \
    ./run-simupop.py -T $T -N $N -r $recomb -u $mut -U $mut -k $nsamp -L $L -l $nsel \
    -g $OUTDIR/run-simupop.log -o $OUTDIR/run-simupop.ped -s $OUTDIR/run-simupop.selloci.txt &> $OUTDIR/run-simupop.time

```

With the parameters above:

```sh

N=1000
T=4000
A=1000
recomb="1e-7"
mut="1e-7"
nsamp=100
L=1000
nsel=$((1 + $L / 1000))
JOBID=$RANDOM

OUTDIR="sim_N_${N}_T_${T}_A_${A}_recomb_${recomb}_mut_${mut}_nsamp_${nsamp}_L_${L}_nsel_${nsel}_run_$JOBID"
mkdir -p $OUTDIR

/usr/bin/time --format="elapsed: %E / kernel: %S / user: %U / mem: %M" \
    ./run-sim.py -T $T -N $N -A $A -r $recomb -u $mut -U $mut -k $nsamp -L $L -l $nsel \
    -g $OUTDIR/run-sim.log -o $OUTDIR/run-sim.vcf -s $OUTDIR/run-sim.selloci.txt -t $OUTDIR/run-sim.trees &> $OUTDIR/run-sim.time

/usr/bin/time --format="elapsed: %E / kernel: %S / user: %U / mem: %M" \
    ./run-simupop.py -T $T -N $N -r $recomb -u $mut -U $mut -k $nsamp -L $L -l $nsel \
    -g $OUTDIR/run-simupop.log -o $OUTDIR/run-simupop.ped -s $OUTDIR/run-simupop.selloci.txt &> $OUTDIR/run-simupop.time

```
