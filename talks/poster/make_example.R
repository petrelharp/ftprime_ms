#!/usr/bin/Rscript

pycode <- '
import msprime
ts = msprime.simulate(8, recombination_rate=2.0)
for j,t in enumerate(ts.trees()):
   t.draw("tree{}.svg".format(j))

ts.dump_text(nodes=open("nodes.txt", "w"), edges=open("edges.txt", "w"))
'

nodes <- read.table("nodes.txt", header=TRUE, fill=TRUE)
edges <- read.table("edges.txt", header=TRUE)

library(xtable)

print(xtable(nodes[,c("id","time")], digits=2), include.rownames=FALSE)
print(xtable(edges, digits=2), include.rownames=FALSE)
