"""
Script to run msprime examples and benchmarks.
"""
import time
import argparse
import os.path
import io
import numpy as np

import msprime

# TODO:
if False:
    # compare speed of pi calc to this:

    ts = msprime.simulate(100)
    G = ts.genotype_matrix()

    def np_pi(ts, G):
      n = ts.num_samples
      m = np.sum(G, 1)
      return sum(2 * m * (n - m) / (n * (n - 1))) / ts.sequence_length

    np.pi(ts, G)



def run_simulation(args):
    before = time.process_time()
    ts = msprime.simulate(
        sample_size=args.sample_size, length=args.length * 10**6, Ne=10**4,
        recombination_rate=1e-8, mutation_rate=1e-8, random_seed=10)
    duration = time.process_time() - before
    print("Ran simulation in {} hours".format(duration / 3600))
    ts.dump(args.file)


def run_newick(args):
    ts = msprime.load(args.file)
    t = next(ts.trees())
    newick = t.newick()
    size = len(newick)
    megabyte = 1024 * 1024
    terabyte = megabyte * 1024 * 1024
    total = size * ts.num_trees
    print("newick size 1 tree    = {:.2f} MiB".format(size / megabyte))
    print("newick size all trees = {:.2f} TiB".format(total / terabyte))


def run_pi(args):
    ts = msprime.load(args.file)
    before = time.process_time()
    pi = ts.get_pairwise_diversity()
    duration = time.process_time() - before
    print("pi = {:.2f}".format(pi))
    print("computed in = {:.2f}s".format(duration))
    # print("newick size all trees = {:.2f} TiB".format(total / terabyte))
    sample_size = 1000
    num_replicates = 10
    all_samples = np.arange(ts.num_samples, dtype=int)
    duration = 0
    for j in range(num_replicates):
        subsample = np.random.choice(all_samples, sample_size, replace=False)
        before = time.process_time()
        pi = ts.get_pairwise_diversity(subsample)
        duration += time.process_time() - before
    duration /= num_replicates
    print("computed subsample pi in average = {:.2f}s".format(duration))


def run_vcf(args):
    ts = msprime.load(args.file)
    total_sites = ts.num_sites
    # Subset the tree sequence down to num_sites.

    t = ts.dump_tables()
    t.sites.set_columns(
        position=t.sites.position[:args.num_sites],
        ancestral_state=t.sites.ancestral_state[:args.num_sites],
        ancestral_state_length=t.sites.ancestral_state_length[:args.num_sites])
    t.mutations.set_columns(
        site=t.mutations.site[:args.num_sites],
        node=t.mutations.node[:args.num_sites],
        derived_state=t.mutations.derived_state[:args.num_sites],
        derived_state_length=t.mutations.derived_state_length[:args.num_sites])
    ts = msprime.load_tables(**t.asdict())
    print("subset down to ", ts.num_sites, "sites")
    megabyte = 1024 * 1024
    terabyte = megabyte * 1024 * 1024
    with io.StringIO() as output:
        ts.write_vcf(output)
        size = output.tell()
    print("Wrote {:.2f} MiB".format(size / megabyte))
    projected = (size / args.num_sites) * total_sites
    print("Estimate {:.2f} TiB".format(projected / terabyte))

def run_stats(args):

    before = time.process_time()
    ts = msprime.load(args.file)
    duration = time.process_time()
    print("Loaded file in {:.2f} seconds".format(duration))
    print("file size  \t {:.2f} MiB".format(os.path.getsize(args.file) / (1024 * 1024)))
    print("num_samples\t", ts.num_samples)
    print("length     \t {} MB".format(ts.sequence_length / 10**6))
    print("num_sites\t", ts.num_sites)
    print("num_trees\t", ts.num_trees)
    before = time.process_time()
    num_trees = 0
    for tree in ts.trees():
        # Just to make sure we do something.
        num_trees += 1
    duration = time.process_time()
    print("tree iter\t {:.2f} seconds".format(duration))
    assert num_trees == ts.num_trees


if __name__ == "__main__":
    # ts_file = "benchmark_ts.hdf5"
    # run_simulation(ts_file)

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subcommand")
    subparsers.required = True

    sim_parser= subparsers.add_parser('simulate')
    sim_parser.add_argument("file")
    sim_parser.add_argument("--sample-size", "-s", type=int, default=500*10**6)
    sim_parser.add_argument("--length", "-l", type=int, default=500)
    sim_parser.set_defaults(func=run_simulation)

    stats_parser = subparsers.add_parser('stats')
    stats_parser.add_argument("file")
    stats_parser.set_defaults(func=run_stats)

    newick_parser = subparsers.add_parser('newick')
    newick_parser.add_argument("file")
    newick_parser.set_defaults(func=run_newick)

    vcf_parser = subparsers.add_parser('vcf')
    vcf_parser.add_argument("file")
    vcf_parser.add_argument("--num-sites", "-s", type=int, default=1000)
    vcf_parser.set_defaults(func=run_vcf)

    pi_parser = subparsers.add_parser('pi')
    pi_parser.add_argument("file")
    pi_parser.add_argument("--num-sites", "-s", type=int, default=1000)
    pi_parser.set_defaults(func=run_pi)

    args = parser.parse_args()
    args.func(args)

