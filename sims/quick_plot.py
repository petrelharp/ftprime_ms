import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

spop = pd.read_csv("simupop_timings.txt", sep="\t")
fp11 = pd.read_csv("cpp_benchmarks/cpp_timings.txt", sep="\t")

spop['engine'] = ['simuPOP'] * len(spop.index)
fp11['engine'] = ['fwdpy11'] * len(fp11.index)

data = pd.concat([spop, fp11])

cmap = matplotlib.cm.get_cmap('viridis')
lcolors = [cmap(0), cmap(125), cmap(cmap.N-25)]
colors = {}
i = 0
for x in sorted(data.N.unique()):
    colors[x] = lcolors[i]
    i = i + 1
ptypes = ['o','^','x']
points = {}
i=0
for x in sorted(data.N.unique()):
    points[x] = ptypes[i]
    i = i+1

data_neut = data[data['sel'] == False].copy(deep=True)

# Plot out the run times for the simulations with selection
data = data[data['sel'] == True]
data.sort_values(by='rho', inplace=True)
groups = data.groupby(['engine', 'arg', 'queue', 'N'])
fig, (ax_fwdpp, ax_fwdpp_arg) = plt.subplots(
    1, 2, sharex=True, sharey=True)
for name, group in groups:
    lstyle = '-'
    if name[0] == 'fwdpy11' and name[1] is False:
        ax = ax_fwdpp
    if name[0] == 'fwdpy11' and name[1] is True:
        ax = ax_fwdpp_arg
    m = points[name[3]]
    if name[0] == 'simuPOP':
        continue
        ax = ax_simupop
        if name[1] is True:
            ax = ax_simupop_arg
    mfacecolor = colors[name[3]]
    if name[2] is True:
        lstyle = 'dashed'
        mfacecolor = 'none'
    popsize = int(name[3])
    ax.plot(group.rho, group.time / (60.**2.), marker=m,
            ms=4, linestyle=lstyle, label=r'$N = {:.0e}$'.format(popsize),
            color=colors[name[3]],
            markerfacecolor=mfacecolor)

ax_fwdpp.legend(loc='upper left',frameon=False)
ax_fwdpp.set_title("With neutral mutations", fontsize='medium')
ax_fwdpp_arg.set_title("With pedigree recording", fontsize='medium')
ax_fwdpp.set_ylabel("Run time (hours)")
ax_fwdpp.set_xlabel('Scaled recombination rate (' + r'$\rho = 4Nr$)')
ax_fwdpp_arg.set_xlabel('Scaled recombination rate (' + r'$\rho = 4Nr$)')
ax_fwdpp_arg.set_xticks([1e3, 1e4, 1e5])
for ax in (ax_fwdpp, ax_fwdpp_arg):
    ax.set_xscale('log')
fig.tight_layout()
plt.savefig("rawspeed.pdf")

# same, on a log scale
data = data[data['sel'] == True]
data.sort_values(by='rho', inplace=True)
groups = data.groupby(['engine', 'arg', 'queue', 'N'])
fig, (ax_fwdpp, ax_fwdpp_arg) = plt.subplots(
    1, 2, sharex=True, sharey=True)
for name, group in groups:
    lstyle = '-'
    if name[0] == 'fwdpy11' and name[1] is False:
        ax = ax_fwdpp
    if name[0] == 'fwdpy11' and name[1] is True:
        ax = ax_fwdpp_arg
    m = points[name[3]]
    if name[0] == 'simuPOP':
        continue
        ax = ax_simupop
        if name[1] is True:
            ax = ax_simupop_arg
    mfacecolor = colors[name[3]]
    if name[2] is True:
        lstyle = 'dashed'
        mfacecolor = 'none'
    popsize = int(name[3])
    ax.plot(group.rho, group.time / (60.**2.), marker=m,
            ms=4, linestyle=lstyle, label=r'$N = {:.0e}$'.format(popsize),
            color=colors[name[3]],
            markerfacecolor=mfacecolor)

ax_fwdpp.legend(loc='upper left',frameon=False)
ax_fwdpp.set_title("With neutral mutations", fontsize='medium')
ax_fwdpp_arg.set_title("With pedigree recording", fontsize='medium')
ax_fwdpp.set_ylabel("Run time (hours)")
ax_fwdpp.set_xlabel('Scaled recombination rate (' + r'$\rho = 4Nr$)')
ax_fwdpp_arg.set_xlabel('Scaled recombination rate (' + r'$\rho = 4Nr$)')
ax_fwdpp_arg.set_xticks([1e3, 1e4, 1e5])
for ax in (ax_fwdpp, ax_fwdpp_arg):
    ax.set_xscale('log')
    ax.set_yscale('log')
fig.tight_layout()
plt.savefig("rawspeed_logy.pdf")


# Plot the relative speedup due to ARG tracking for the sims with selection

data_arg = data[(data['arg'] == True) & (data['queue'] == False)].copy()
data_noarg = data[(data['arg'] == False) & (data['queue'] == False)].copy()
data_queue = data[data['queue'] == True].copy()
joined = data_arg.merge(data_noarg, on=[
                        'engine', 'N', 'rho'], how='outer', suffixes=('_arg', '_noarg')).dropna()
joined['speedup'] = joined['time_noarg'] / joined['time_arg']
groups = joined.groupby(['engine', 'N'])
fig, (ax_fwdpp) = plt.subplots(
    1,  sharex=True, sharey=False)
for name, group in groups:
    lstyle = 'solid'
    if name[0] == 'fwdpy11':
        ax = ax_fwdpp
    m = points[name[1]]
    if name[0] == 'simuPOP':
        continue
        ax = ax_simupop
    mfacecolor = colors[name[1]]
    popsize = int(name[1])
    ax.plot(group.rho, group.speedup, marker=m,
            ms=4, linestyle=lstyle, label=r'$N = {:.0e}$'.format(popsize),
            color=colors[name[1]],
            markerfacecolor=mfacecolor)

for ax in (ax_fwdpp,):
    ax.set_ylabel("Speedup due to\npedigree recording")
ax_fwdpp.set_xlabel('Scaled recombination rate (' + r'$\rho = 4Nr$)')
ax_fwdpp.set_xscale('log')
ax_fwdpp.legend(loc='best',frameon=False)
fig.tight_layout()
plt.savefig("speedup.pdf")

# Now, plots for sims w/o selection
data_neut.sort_values(by='rho', inplace=True)
groups = data_neut.groupby(['engine', 'arg', 'queue', 'N'])
fig, ((ax_fwdpp, ax_fwdpp_arg), (ax_simupop, ax_simupop_arg)) = plt.subplots(
    2, 2, sharex=True, sharey=True)
for name, group in groups:
    lstyle = 'solid'
    if name[0] == 'fwdpy11' and name[1] is False:
        ax = ax_fwdpp
    if name[0] == 'fwdpy11' and name[1] is True:
        print(group)
        ax = ax_fwdpp_arg
    m = points[name[3]]
    if name[0] == 'simuPOP':
        ax = ax_simupop
        if name[1] is True:
            ax = ax_simupop_arg
    mfacecolor = colors[name[3]]
    if name[2] is True:
        lstyle = 'dashed'
        mfacecolor = 'none'
    popsize = int(name[3])
    ax.plot(group.rho, group.time / (60.**2.), marker=m,
            ms=4, linestyle=lstyle, label=r'$N = {:.0e}$'.format(popsize),
            color=colors[name[3]],
            markerfacecolor=mfacecolor)

ax_fwdpp.legend(loc='upper left',frameon=False)
ax_fwdpp.set_title("fwdpy11 with neutral mutations", fontsize='medium')
ax_fwdpp_arg.set_title("fwdpy11 with pedigree recording", fontsize='medium')
ax_simupop.set_ylabel("Run time (hours)")
ax_fwdpp.set_ylabel("Run time (hours)")
ax_simupop.set_title("simuPOP with neutral mutations", fontsize='medium')
ax_simupop_arg.set_title("simuPOP with pedigree recording", fontsize='medium')
ax_simupop.set_xlabel('Scaled recombination rate (' + r'$\rho = 4Nr$)')
ax_simupop_arg.set_xlabel('Scaled recombination rate (' + r'$\rho = 4Nr$)')
ax_simupop_arg.set_xticks([1e3, 1e4, 1e5])
for ax in (ax_simupop, ax_simupop_arg):
    ax.set_xscale('log')
fig.tight_layout()
plt.savefig("rawspeed_nosel.pdf")

# Relative speedup for sims w/o selection
data_arg = data_neut[(data_neut['arg'] == True) &
                     (data_neut['queue'] == False)].copy()
data_noarg = data_neut[(data_neut['arg'] == False) &
                       (data_neut['queue'] == False)].copy()
joined = data_arg.merge(data_noarg, on=[
                        'engine', 'N', 'rho'], how='outer', suffixes=('_arg', '_noarg')).dropna()
joined['speedup'] = joined['time_noarg'] / joined['time_arg']
groups = joined.groupby(['engine', 'N'])
fig, (ax_fwdpp, ax_simupop) = plt.subplots(
    2,  sharex=True, sharey=False)
for name, group in groups:
    lstyle = 'solid'
    if name[0] == 'fwdpy11':
        ax = ax_fwdpp
    m = points[name[1]]
    if name[0] == 'simuPOP':
        ax = ax_simupop
    mfacecolor = colors[name[1]]
    popsize = int(name[1])
    ax.plot(group.rho, group.speedup, marker=m,
            ms=4, linestyle=lstyle, label=r'$N = {:.0e}$'.format(popsize),
            color=colors[name[1]],
            markerfacecolor=mfacecolor)

for ax in (ax_fwdpp, ax_simupop):
    ax.set_ylabel("Speedup due to\npedigree recording")
ax_fwdpp.set_title("fwdpy11", fontsize='medium')
ax_simupop.set_title("simuPOP", fontsize='medium')
ax_simupop.set_xlabel('Scaled recombination rate (' + r'$\rho = 4Nr$)')
ax_simupop.set_xscale('log')
ax_fwdpp.legend(loc='best',frameon=False)
fig.tight_layout()
plt.savefig("speedup_nosel.pdf")
