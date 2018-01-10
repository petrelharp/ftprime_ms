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
    1, 2, sharex=True, sharey=False)
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
    ax.plot(group.rho, group.mem / (1024.**2.), marker=m,
            ms=4, linestyle=lstyle, label=r'$N = {:.0e}$'.format(popsize),
            color=colors[name[3]],
            markerfacecolor=mfacecolor)

ax_fwdpp.legend(loc='best',frameon=False)
ax_fwdpp.set_title("fwdpy11 with neutral mutations", fontsize='medium')
ax_fwdpp_arg.set_title("fwdpy11 with pedigree tracking", fontsize='medium')
ax_fwdpp.set_ylabel("Peak RAM use (GB)")
ax_fwdpp.set_xlabel('Scaled recombination rate (' + r'$\rho = 4Nr$)')
ax_fwdpp_arg.set_xlabel('Scaled recombination rate (' + r'$\rho = 4Nr$)')
ax_fwdpp_arg.set_xticks([1e3, 1e4, 1e5])
ax_fwdpp.set_xticks([1e3, 1e4, 1e5])
for ax in (ax_fwdpp, ax_fwdpp_arg):
    ax.set_xscale('log')
fig.tight_layout()
plt.savefig("memuse.pdf")

# Now, plots for sims w/o selection
data_neut.sort_values(by='rho', inplace=True)
groups = data_neut.groupby(['engine', 'arg', 'queue', 'N'])
fig, (ax_fwdpp, ax_fwdpp_arg) = plt.subplots(
    1, 2, sharex=True, sharey=True)
for name, group in groups:
    lstyle = 'solid'
    if name[0] == 'fwdpy11' and name[1] is False:
        ax = ax_fwdpp
    if name[0] == 'fwdpy11' and name[1] is True:
        print(group)
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
    ax.plot(group.rho, group.mem / (1024.**2.), marker=m,
            ms=4, linestyle=lstyle, label=r'$N = {:.0e}$'.format(popsize),
            color=colors[name[3]],
            markerfacecolor=mfacecolor)

ax_fwdpp.legend(loc='upper left',frameon=False)
ax_fwdpp.set_title("fwdpy11 with neutral mutations", fontsize='medium')
ax_fwdpp_arg.set_title("fwdpy11 with pedigree tracking", fontsize='medium')
ax_fwdpp.set_ylabel("Peak RAM use (GB)")
ax_fwdpp.set_xlabel('Scaled recombination rate (' + r'$\rho = 4Nr$)')
ax_fwdpp_arg.set_xlabel('Scaled recombination rate (' + r'$\rho = 4Nr$)')
ax_fwdpp_arg.set_xticks([1e3, 1e4, 1e5])
ax_fwdpp.set_xticks([1e3, 1e4, 1e5])
for ax in (ax_fwdpp, ax_fwdpp_arg):
    ax.set_xscale('log')
fig.tight_layout()
plt.savefig("memuse_nosel.pdf")
