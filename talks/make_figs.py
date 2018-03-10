import msprime
import os

if not os.path.exists("sim_ts"):
    os.makedirs("sim_ts")

ts = msprime.simulate(5, length=1, recombination_rate=5, random_seed=23)

for k, t in enumerate(ts.trees()):
    t.draw(path="sim_ts/sim_ts.{0:03d}.svg".format(k))

