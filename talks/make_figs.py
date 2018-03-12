import msprime
import os
import wf

### a tree sequence

if not os.path.exists("sim_ts"):
    os.makedirs("sim_ts")

ts = msprime.simulate(30, length=1, recombination_rate=5, random_seed=23)

for k, t in enumerate(ts.trees()):
    t.draw(path="sim_ts/sim_ts.{0:03d}.svg".format(k), width=600)

# let make know we're done
open("sim_ts/done", "w").close()

### a WF tree sequence

ts = wf.wright_fisher(10, 0.5, 1.0, 30)
labels = {u.id:"" for u in ts.nodes()}
for k, u in enumerate(ts.samples()):
    labels[u] = str(k)

if not os.path.exists("sim_wf"):
    os.makedirs("sim_wf")

for k, t in enumerate(ts.trees()):
    t.draw(path="sim_wf/sim_wf.{0:03d}.svg".format(k), 
           width=600, height=300)

# let make know we're done
open("sim_ts/done", "w").close()

if not os.path.exists("sim_wf_unlabeled"):
    os.makedirs("sim_wf_unlabeled")

for k, t in enumerate(ts.trees()):
    t.draw(path="sim_wf_unlabeled/sim_wf.{0:03d}.svg".format(k), 
           node_label_text=labels, 
           width=600, height=300)

# let make know we're done
open("sim_wf_unlabeled/done", "w").close()

### a simplified WF tree sequence

if not os.path.exists("sim_wf_simplified"):
    os.makedirs("sim_wf_simplified")

ts = ts.simplify()

for k, t in enumerate(ts.trees()):
    t.draw(path="sim_wf_simplified/sim_wf.{0:03d}.svg".format(k), 
           internal_node_labels=False,
           width=600, height=300)

# let make know we're done
open("sim_wf_simplified/done", "w").close()
