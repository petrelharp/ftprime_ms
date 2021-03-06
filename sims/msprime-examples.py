"""
Script to run msprime examples and benchmarks.
"""
import time
import argparse
import os.path
import io
import numpy as np

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

import msprime


def run_simulation(args):
    before = time.process_time()
    print("Running sim for n = ", args.sample_size, "l = ", args.length)
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
    print("variant matrix size\t", ts.num_sites * ts.num_samples / (1024**3), "GiB")
    before = time.process_time()
    num_trees = 0
    for tree in ts.trees():
        # Just to make sure we do something.
        num_trees += 1
    duration = time.process_time()
    print("tree iter\t {:.2f} seconds".format(duration))
    assert num_trees == ts.num_trees


def run_simplify_subsample_size_benchmark(args):
    ts = msprime.load(args.file)
    np.random.seed(1)
    print("Running simplify benchmarks")
    N = 20
    num_replicates = 5
    subsample_size = np.logspace(1, 5, N).astype(int)
    print(subsample_size)
    T = np.zeros(N)
    for j in range(N):
        X = np.zeros(num_replicates)
        for k in range(num_replicates):
            sample = np.random.choice(
                ts.num_samples, subsample_size[j], replace=False).astype(np.int32)
            before = time.process_time()
            sub_ts = ts.simplify(sample)
            X[k] = time.process_time() - before
        T[j] = np.mean(X)
        print(subsample_size[j], T[j])

    df = pd.DataFrame({"subsample_size": subsample_size, "time": T})
    df.to_csv("data/simplify_subsample.dat")

    plt.semilogx(subsample_size, T, marker="o")
    plt.xlabel("Subsample size")
    plt.ylabel("Time to simplify (s)")
    plt.savefig("simplify_subsample_perf.pdf", format='pdf')


def run_simplify_num_edges_benchmark(args):
    ts = msprime.load(args.file)
    np.random.seed(1)
    print("num_nodes = ", ts.num_nodes)
    print("num_edges = ", ts.num_edges)
    num_slices = 10

    tables = ts.dump_tables()
    nodes = tables.nodes
    edges = tables.edges

    node_time = nodes.time
    left = edges.left
    right = edges.right
    parent = edges.parent
    child = edges.child

    size = left.nbytes + right.nbytes + parent.nbytes + child.nbytes
    print("Total edge size = ", size / 1024**3, "GiB")
    sample_sizes = [10, 100, 1000]
    num_sample_sizes = len(sample_sizes)

    num_edges = np.zeros(num_slices * num_sample_sizes)
    simplify_time = np.zeros(num_slices * num_sample_sizes)
    sample_size = np.zeros(num_slices * num_sample_sizes)
    slice_size = ts.num_edges // num_slices

    j = 0
    for N in sample_sizes:
        for start in range(ts.num_edges - slice_size, 0, -slice_size):
            max_node = np.max(child[start:])
            samples = np.arange(max_node - N, max_node, dtype=np.int32)
            subset_nodes = msprime.NodeTable()
            subset_nodes.set_columns(
                time=node_time[:max_node + 1], flags=np.ones(max_node + 1, dtype=np.uint32))
            subset_edges = msprime.EdgeTable()
            subset_edges.set_columns(
                left=left[start:], right=right[start:], parent=parent[start:],
                child=child[start:])
            before = time.process_time()
            msprime.simplify_tables(samples=samples, nodes=subset_nodes, edges=subset_edges)
            duration = time.process_time() - before
            num_edges[j] = ts.num_edges - start
            simplify_time[j] = duration
            sample_size[j] = N
            print(N, num_edges[j], duration, num_edges[j] / duration, "per second")
            j += 1

    df = pd.DataFrame(
        {"sample_size": sample_size, "num_edges": num_edges, "time": simplify_time})
    df.to_csv("data/simplify_num_edges.dat")

    for N in sample_sizes:
        index = sample_size == N

        plt.plot(num_edges[index], simplify_time[index], marker="o")
        plt.xlabel("num edges")
        plt.ylabel("Time to simplify (s)")
        plt.savefig("simplify_num_edges.png")


def run_benchmark_pi(args):
    before = time.process_time()
    ts = msprime.simulate(
        sample_size=args.sample_size, length=args.length * 10**6, Ne=10**4,
        recombination_rate=1e-8, mutation_rate=1e-8, random_seed=10)
    duration = time.process_time() - before
    print("Ran simulation in {} seconds".format(duration))
    print("sample size = ", ts.sample_size)
    print("num_sites = ", ts.num_sites)

    G = ts.genotype_matrix()
    print("Genotype matrix = ", G.nbytes / 1024**3, "GB")

    def np_pi(G):
        n = ts.num_samples
        m = np.sum(G, 1)
        return sum(2 * m * (n - m) / (n * (n - 1)))

    before = time.process_time()
    pi1 = np_pi(G)
    np_time = time.process_time() - before
    print("np time = ", np_time)

    before = time.process_time()
    pi2 = ts.get_pairwise_diversity()
    msp_time = time.process_time() - before
    print("msp time = ", msp_time)
    print("pi values = ", pi1, pi2)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subcommand")
    subparsers.required = True

    subparser = subparsers.add_parser('simulate')
    subparser.add_argument("file")
    subparser.add_argument("--sample-size", "-s", type=int, default=5*10**5)
    subparser.add_argument("--length", "-l", type=int, default=200)
    subparser.set_defaults(func=run_simulation)

    subparser = subparsers.add_parser('stats')
    subparser.add_argument("file")
    subparser.set_defaults(func=run_stats)

    subparser = subparsers.add_parser('newick')
    subparser.add_argument("file")
    subparser.set_defaults(func=run_newick)

    subparser = subparsers.add_parser('vcf')
    subparser.add_argument("file")
    subparser.add_argument("--num-sites", "-s", type=int, default=1000)
    subparser.set_defaults(func=run_vcf)

    subparser = subparsers.add_parser('pi')
    subparser.add_argument("file")
    subparser.add_argument("--num-sites", "-s", type=int, default=1000)
    subparser.set_defaults(func=run_pi)

    subparser = subparsers.add_parser('simplify-subsample')
    subparser.add_argument("file")
    subparser.set_defaults(func=run_simplify_subsample_size_benchmark)

    subparser = subparsers.add_parser('simplify-num-edges')
    subparser.add_argument("file")
    subparser.set_defaults(func=run_simplify_num_edges_benchmark)

    subparser = subparsers.add_parser('benchmark-pi')
    subparser.add_argument("--sample-size", "-s", type=int, default=2 * 10**5)
    subparser.add_argument("--length", "-l", type=int, default=100)
    subparser.set_defaults(func=run_benchmark_pi)

    args = parser.parse_args()
    args.func(args)

