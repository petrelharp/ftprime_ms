---
title: "Efficient pedigree recording for fast population genetics simulation"
author: "Jerome Kelleher, Kevin Thornton, Jaime Ashander, and Peter Ralph (*me*)"
date: "12 March 2018 :: [bioRxiv](https://www.biorxiv.org/content/early/2018/01/16/248500)"
---

This talk: [slides here](https://petrelharp.github.io/ftprime_ms/broad_12_mar_2018.slides.html)

1. what are tree sequences and what are they good for
2. explain application to forwards simulation recording
3. display impressive speedups


<!-- 1. explain tree sequences and why they are so efficient (5min) -->
# The tree sequence

## History is a sequence of trees

For a set of sampled chromosomes,
at each position along the genome there is a genealogical tree
that says how they are related.

![Trees along a chromosome](sim_ts.anim.gif)


----------------------

A **tree sequence** describes this, er, sequence of trees.

. . .

*Observations:*

1. The *pedigree* (parental relationships) plus crossover locations
    would give us the tree sequence for *everyone, ever*.

2. Much less can fully describe the history relevant to a *sample* of genomes.

3. This information is equivalent to the Ancestral Recombination Graph (ARG).


-------------

[Kelleher, Etheridge, and McVean](http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004842) 
introduced the **tree sequence** data structure
for a fast coalescent simulator, [msprime](https://github.com/jeromekelleher/msprime).

- stores genealogical *and* variation data **very** compactly

- efficient algorithms available:

    * subsetting
    * calculation of allele frequencies in arbitrary cohorts
    * linkage disequilibrium
    * log-time haplotype matching

- tree-based sequence storage closely related to haplotype-matching compression


## Simulated file sizes

::: {.columns}
::::::: {.column width="50%"}

![file sizes](file_size.png)

:::
::::::: {.column width="50%"}

- HapMap chr1 genetic map (250Mb)
- Gutenkunst et al out-of-Africa model (3 pops)
- mutation rate $2 \times 10^{-8}$ per gen
- at $n=10^7$ 

    * about 17 million variants
    * VCF size: 318 TiB (250,000$\times$ larger)

:::
:::::::

## Example: three samples; two trees; two variant sites

![Example tree sequence](example_tree_sequence.png)

-----------------------

Storing a tree sequence in
the four tables - *nodes*, *edges*, *sites*, and *mutations* -
is *succinct* (no redundancy).

. . .

These are stored efficiently (hdf5) on disk
with a bit more information (e.g., metadata).


## Nodes and edges

Edges 

:   Common ancestor (i.e., coalescent) events.

    Records: interval (left, right); parent node; child node.

Nodes 

:   The ancestors those happen in.

    Records: time ago (of birth); ID (implicit).

-------------------

![Building a tree sequence](nodes_edges_walkthrough/nodes_edges_walkthrough.0.png)

-------------------


![Building a tree sequence](nodes_edges_walkthrough/nodes_edges_walkthrough.1.png)

-------------------


![Building a tree sequence](nodes_edges_walkthrough/nodes_edges_walkthrough.2.png)

-------------------


![Building a tree sequence](nodes_edges_walkthrough/nodes_edges_walkthrough.3.png)

-------------------


![Building a tree sequence](nodes_edges_walkthrough/nodes_edges_walkthrough.4.png)

-------------------


![Building a tree sequence](nodes_edges_walkthrough/nodes_edges_walkthrough.5.png)

-------------------

![Building a tree sequence](nodes_edges_walkthrough/nodes_edges_walkthrough.6.png)


## Sites and mutations

Mutations

:   When state changes along the tree.

    Records: site it occured at; derived state.

Sites 

:   Where mutations fall on the genome.

    Records: genomic position; ancestral (root) state; ID (implicit).


------------------

![Adding mutations](sites_muts_walkthrough/sites_muts_walkthrough.0.png)

------------------

![Adding mutations](sites_muts_walkthrough/sites_muts_walkthrough.1.png)

------------------

![Adding mutations](sites_muts_walkthrough/sites_muts_walkthrough.2.png)

------------------

![Adding mutations](sites_muts_walkthrough/sites_muts_walkthrough.3.png)

------------------

![Adding mutations](sites_muts_walkthrough/sites_muts_walkthrough.4.png)



<!-- 3. recall uses for fwds sims (2min) -->
# Forwards simulations

## Why forwards simulations?

Coalescent simulations are *much faster*
than forwards-time, individual-based simulations

. . .

because they don't have to keep track of *everyone*,
only the ancestors of your sample.

. . .

**But:** selection, or sufficient geographic structure,
break the assumptions of coalescent theory.

## Geography or selection break coalescent theory

So, if you

1. have more than a couple of loci under selection, and/or
2. have fine enough scale geography that demographic fluctuations are important
    (e.g., continuous space)

then you have to do forwards-time, individual-based simulations.

---------------------------

To model linked selection,
we need chromosome-scale simulations.

. . .

Then every individual needs to carry around her genotype (somehow).
Even at neutral sites!

. . .

**Bummer.**

. . .

*But wait...*


<!-- 4. explain application to fwds sim recording (5min) -->
# Forwards-time tree sequence recording

## The main idea

If we *record the tree sequence*
that relates everyone to everyone else,

after the simulation is over we can put neutral mutations down on the trees.

. . .

Since neutral mutations don't affect demography,

this is *equivalent* to having kept track of them throughout.

------------

This means recording the entire genetic history of **everyone** in the population, **ever**.

.  . .

It is *not* clear this is a good idea.


## Tree recording strategy

Every time an individual is born, we must:

::: incremental

1. add each gamete to the Node Table,
2. add entries to the Edge Table
    recording which parent each gamete inherited each bit of genome from, and
3. add any new selected mutations to the Mutation Table 
    and (if necessary) their locations to the Site Table.

:::

. . .

::: {.columns}
:::::: {.column width=15%}

![Rightarrow](finger_right.png){width="100%"}

:::
:::::: {.column width=5%}

:::
:::::: {.column width=75%}

This produces **waaaaay** too much data.

:::
::::::

-------------------

We won't end up needing the *entire* history
of *everyone ever*,

. . .

but we won't know *what* we'll need until later.

. . .

How do we get rid of the extra stuff?


## Simplification

*Question:* given a tree sequence
containing the history of many individuals,
how do we *simplify* it to only the history
of a subset?

-----------

Concretely, given an input tree sequence
and a subset of its nodes we call the *samples*,
we want a new tree sequence for which:

1. All marginal trees match the corresponding subtree 
    in the input tree sequence.

2. Every non-sample node in marginal trees has at least two children.

3. All nodes and edges are ancestral to at least one sample.

4. No adjacent redundant edges 
    (e.g., $(\ell, x, p, c) + (x, r, p, c) \rightarrow (\ell, r, p, c)$).

-----------

*Answer:* to simplify a tree sequence
to the history of the *samples*:

1. Paint each *sampled* chromosome a distinct color.

2. Moving back up the tree sequence,
    copy colors of each chromosome to the parental chromosomes
    they inherited from.

3. If two colors go in the same spot (*coalescence*),
    replace with a new color (unique to that ancestor).
    Output a node for the ancestor and an edge for the coalescence.)

4. Once all colors have coalesced in a given segment,
    stop propagating it.

## An example: simplify these to J and K

![Simplify example](simplify_walkthrough.png){ width="100%" }

-------------------

![Simplify example](simplify_walkthrough/simplify_walkthrough.0.png){ width="100%" }

-------------------

![Simplify example](simplify_walkthrough/simplify_walkthrough.1.png){ width="100%" }

-------------------

![Simplify example](simplify_walkthrough/simplify_walkthrough.2.png){ width="100%" }

-------------------

![Simplify example](simplify_walkthrough/simplify_walkthrough.3.png){ width="100%" }

-------------------

![Simplify example](simplify_walkthrough/simplify_walkthrough.4.png){ width="100%" }

-------------------

![Simplify example](simplify_walkthrough/simplify_walkthrough.5.png){ width="100%" }

-------------------

![Simplify example](simplify_walkthrough/simplify_walkthrough.6.png){ width="100%" }

-------------------

![Simplify example](simplify_walkthrough/simplify_walkthrough.7.png){ width="100%" }

-------------------

![Simplify example](simplify_walkthrough/simplify_walkthrough.8.png){ width="100%" }

-------------------

![Simplify example](simplify_walkthrough/simplify_walkthrough.9.png){ width="100%" }

-------------------

![Simplify example](simplify_walkthrough/simplify_walkthrough.10.png){ width="100%" }

-------------------

![Simplify example](simplify_walkthrough/simplify_walkthrough.11.png){ width="100%" }

-------------------

![Simplify example](simplify_walkthrough/simplify_walkthrough.12.png){ width="100%" }

-------------------

![Simplify example](simplify_walkthrough/simplify_walkthrough.13.png){ width="100%" }

-------------------

![Simplify example](simplify_walkthrough/simplify_walkthrough.14.png){ width="100%" }

-------------------

![Simplify example](simplify_walkthrough/simplify_walkthrough.15.png){ width="100%" }


## Wright-Fisher, N=10: before simplification

![Wright-Fisher tree sequence](sim_wf.anim.gif)

## Wright-Fisher, N=10: before simplification

![Wright-Fisher tree sequence](sim_wf_unlabeled.anim.gif)

## ... and after simplification

![Simplified Wright-Fisher tree sequence](sim_wf_simplified.anim.gif)


## *Revised* tree recording strategy

Every time an individual is born, we must:


1. add each gamete to the Node Table,
2. add entries to the Edge Table
    recording which parent each gamete inherited each bit of genome from
3. add any new mutations to the Mutation Table 
    and (if necessary) their locations to the Site Table.

... and,

4. Every so often, *simplify* the tables so far,
    retaining the history of the current generation.


<!-- 5. display impressive speedups 2min) -->
# Implementation and results

## Benchmark implementation

- Recording, simplifying, and output of tables: 
    `C` code in `msprime`. (soon: `tskit`)

- Simulation: [`fwdpp`](https://github.com/molpopgen/fwdpp), by Kevin Thornton (in `C++`) ([code](https://github.com/molpopgen/fwdpy11_arg_example))

- Glue: [`pybind11`](https://github.com/pybind/pybind11/) and [`numpy`](http://www.numpy.org/)

- Machine: Ubuntu / 2x 2.6 GHz Intel E5-2650 CPU

. . .

*Other implementations:* 

- [pure `python`](https://github.com/ashander/ftprime), interfacing with [`simuPOP`](https://github.com/BoPeng/simuPOP)
- [cython](https://github.com/molpopgen/tutorials/blob/cython_cpp_tutorial/notebooks/wfcython.ipynb)

## Simulation parameters

1. Wright-Fisher population of size $N$
2. simulated for $10N$ genreations
3. neutral mutation rate $\mu$ equal to recombination rate $r$ per gamete
4. many, weakly deleterious mutations: rate $\mu/100$ with
    $s$ exponentially distributed with mean $2.5/N$.

. . .

*Note:*
if we recorded tree sequences ("pedigree recording")
then the neutral mutation rate was *zero*
but neutral mutations were added *afterwards*.


--------------------------

![Total run time per single simulation as a function of region length.](rawspeed.png){ width=80% }

--------------------------

![Relative speedup of simulations](speedup.png){ width=80% }



## Memory use

RAM requirements are determined by how often you simplify.


<!-- 6. advertise other reasons to have output in tree sequences (2min) -->

# Moving forward

<!-- 2. advertise tskit (1min) -->
## tskit : a toolkit for tree sequences

Tools in `msprime`
can do these things "very fast":

1. Read in: tables $\rightarrow$ tree sequence
2. Write out: tree sequence $\rightarrow$ tables
3. Iterate over trees,
4. while computing some statistic (AFS, $\pi$, $f_4$, LD, \ldots).
5. Simplify (i.e., subset).

. . .

*Upcoming:* will be moved to [*tskit*](https://github.com/tskit-dev/tskit).


## tsinfer :: real data in tree sequences

In progress: *tsinfer* (Kelleher, Wong, and McVean)
infers tree sequences from real genomic data.

Watch Jerome's talk:
[Simulating, storing & processing genetic variation data w/millions of samples](https://www.youtube.com/watch?v=MH2b9iU4oUA)


## Tree sequences ...

1. are compact, useful ways to store population history
    *including* genome sequence.

2. can be succinctly encoded in a set of tables,
    which we provide tools for using.

3. can be output during a forwards-time simulation,

4. which not only gets you trees in the end,
    but also makes much larger simulations possible.


## Future uses

1. Machine learning needs *good*, *fast* simulations to train on.

2. Tree sequences allow quick computation of many genomic statistics
    from real data.

. . .

*Current work:* tree sequence recording in [SLiM](https://messerlab.org/slim/)
(with Jared Galloway).


# Thanks

## Acknowledgements

Funding: NSF (PR); Wellcome Trust (JK); NIH (KRT); USF&WS (JDA).

Slides with [reveal.js](http://hakim.se) and [pandoc](https://pandoc.org/).

