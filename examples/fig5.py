# coding: utf-8
import msprime

ts = msprime.load_text(edges=open('edges_full.txt'),
                       nodes=open('nodes_full.txt'))
full_node_map = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H',
                 8: 'I', 9: 'J', 10: 'K'}

print("Full trees")
for t in ts.trees():
    print(t.draw(format='unicode', node_label_text=full_node_map))


print("Simplifed trees with to J (9), K (10) with `ts.simplify()`)")
tss = ts.simplify(samples=[9, 10])
for t in tss.trees():
    print(t.draw(format='unicode'))


print("Simplifed trees from tables in fig 5C",
      "with J (0) and K(1) marked as samples.")
tss2 = msprime.load_text(edges=open('edges.txt'), nodes=open('nodes.txt'))
for t in tss2.trees():
    print(t.draw(format='unicode'))

print("Raw tables from `ts.simplify()`:")
print(tss.dump_tables())
print("\n\n\n...and from the trees loaded from text tables:")
print(tss2.dump_tables())
