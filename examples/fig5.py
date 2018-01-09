# coding: utf-8
import msprime
print("Simplifed trees")
ts = msprime.load_text(edges=open('edges.txt'), nodes=open('nodes.txt'))
for t in ts.trees():
    print(t.draw(format='unicode'))
