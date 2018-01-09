# coding: utf-8
import msprime

ts = msprime.load_text(edges=open('edges_full.txt'),
                       nodes=open('nodes_full.txt'))
full_node_map = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H',
                 8: 'I', 9: 'J', 10: 'K'}

print("Full trees")
for t in ts.trees():
    print(t.draw(format='unicode', node_label_text=full_node_map))

print("Simplifed trees")
tss = msprime.load_text(edges=open('edges.txt'), nodes=open('nodes.txt'))
for t in tss.trees():
    print(t.draw(format='unicode'))
