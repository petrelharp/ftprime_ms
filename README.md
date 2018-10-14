# Resources for Kelleher et al., "Efficient pedigree recording for fast population genetics simulation"

* The C++ source code used in the paper is found in the fwdpy11_arg_example folder of this repository.  The contents of
  that directory are a simple copy of what can be found in the
  [repository](https://github.com/molpopgen/fwdpy11_arg_example) where it was developed.  You will find instructions in
  the README of that subdirectory.
* The flexible Python implementation (which uses `simuPOP`) is available in the [`ftprime` repository as version 0.0.6](https://github.com/ashander/ftprime/tree/0.0.6)
* We have generated a set of [tutorials](https://tskit-dev.github.io/tutorials/) on integrating forward simulations with the simplification algorithm as
  implemented in [msprime](https://msprime.readthedocs.io/en/stable/)

## Reproducibility

The results in this paper were generated with what ultimately became msprime version 0.5.0. The current version of
msprime (0.6.x) contains a faster and more streamlined version of the algorithm that gives the same results.

## Algorithm reference implementations

We provide some reference implementations of the algorithms described in the paper. To ensure that 
these will work as easily as possible in the future, they require mprime >= 0.6.0.

* The file ``sims/simplify-alg.py`` contains a direct Python implementation of the simplify 
  algorithm (algorithm S).


* The file ``sims/wf-figures.py`` contains a direct Python implementation of Wright-Fisher 
  forwards time simulation (algorithm W).
