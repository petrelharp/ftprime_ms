# To-do, 11/7:

## Methods

- inkscape fig 1

- add outline of how to use tree differences to SPR to section of tree seqs

- fill in section on the simplify algorithm, with (a) general idea involving coloring in chromosomes; and (b) more detail (signposted)

- maybe move API section to discussion, maybe not; either way add sentence to abstract

## Results

- general structure: (1) estimates and analytical results, (2) practical measurements

- for simple WF alg with exactly one recomb per gen, should be 2Nt edges; post-simplification should be 2N log N * rho edges
    because each tree change is the start of a new edge;
    since 2N log N is also the number of segregating sites, this same thing gives us the computation for mutations

    * move stuff on mutations from methods to here

    * make plots of scaling from WF sim: maybe put plots in appx?


# Earlier notes

- merge current drafts of the paper and make more of a skeleton [Peter]

- to describe the method we will write out the simple WF simulation from tests/ and say that sequential simplify is important but just bookkeeping [Peter]

- benchmark time spent in msprime versus in simulation [kevin]

- investigate the effect of the simplify interval [kevin]

- write out the simplify algorithm [Jerome]

- make a plot of simulation timing, with log N on the x axis, and time per generation on the y, in each case doing a single chromosome with selected mutation rate low enough that we get on order of tens of selected mutations.
    * figure out parameter values and tell Jaime [Kevin]
    * run this also in SimuPOP [Jaime]
