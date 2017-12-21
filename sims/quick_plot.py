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
#lcolors = ['black', 'green', 'blue']
lcolors = [cmap(0.25), cmap(0.5), cmap(0.75)]
colors = {}
i = 0
for x in sorted(data.N.unique()):
    colors[x] = lcolors[i]
    i = i + 1


data = data[data['sel'] == True]
data.sort_values(by='rho', inplace=True)
groups = data.groupby(['engine', 'arg', 'queue', 'N'])
fig, ((ax_fwdpp, ax_fwdpp_arg), (ax_simupop, ax_simupop_arg)) = plt.subplots(
    2, 2, sharex=True, sharey=True)
for name, group in groups:
    lstyle = 'solid'
    if name[0] == 'fwdpy11' and name[1] is False:
        ax = ax_fwdpp
    if name[0] == 'fwdpy11' and name[1] is True:
        ax = ax_fwdpp_arg
    m = 'o'
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
            ms=4, linestyle=lstyle, label=r'$N = {}$'.format(popsize),
            color=colors[name[3]],
            markerfacecolor=mfacecolor)

ax_fwdpp.legend(loc='best')
ax_fwdpp.set_title("fwdpy11 with neutral mutations")
ax_fwdpp_arg.set_title("fwdpy11 with ancestry tracking")
ax_simupop.set_ylabel("Run time (hours)")
ax_fwdpp.set_ylabel("Run time (hours)")
ax_simupop.set_title("simuPOP with neutral mutations")
ax_simupop_arg.set_title("simuPOP with ancestry tracking")
ax_simupop.set_xlabel('Scaled recombination rate (' + r'$\rho = 4Nr$)')
ax_simupop_arg.set_xlabel('Scaled recombination rate (' + r'$\rho = 4Nr$)')
ax_simupop_arg.set_xticks([1e3, 1e4, 1e5])
for ax in (ax_simupop, ax_simupop_arg):
    ax.set_xscale('log')
    for tick in ax.get_xticklabels():
        tick.set_rotation(45)
    # ax.ticklabel_format(style='sci', axis='x', scilimits=(-3,0))
# ax.set_yscale("log")
# plt.legend(bbox_to_anchor=(1.05, 1), loc=2)
# plt.xlabel('Scaled recombination rate (' + r'$\rho = 4Nr$)')
fig.tight_layout()
# plt.ticklabel_format(style='sci', axis='x', scilimits=(0,2))
plt.savefig("rawspeed.pdf")

fig, (ax_fwdpp, ax_fwdpp_arg, ax_simupop, ax_simupop_arg) = plt.subplots(
    4, sharex=True, sharey=True)
# ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling
for name, group in groups:
    lstyle = 'solid'
    ax = ax_fwdpp
    if name[0] == 'fwdpy11' and name[1] is True:
        ax = ax_fwdpp_arg
    m = 'o'
    if name[0] == 'simuPOP':
        ax = ax_simupop
        if name[1] is True:
            ax = ax_simupop_arg
    mfacecolor = colors[name[3]]
    if name[2] is True:
        lstyle = 'dashed'
        mfacecolor = 'none'
    popsize = int(name[3])
    ax.plot(group.rho, group.mem / (1024.**2.), marker=m,
            ms=6, linestyle=lstyle, label=r'$N = {}$'.format(popsize),
            color=colors[name[3]],
            markerfacecolor=mfacecolor)

ax_fwdpp.legend(loc='best')
ax_fwdpp.set_title("fwdpy11 with neutral mutations")
ax_fwdpp_arg.set_title("fwdpy11 with ancestry tracking")
ax_fwdpp_arg.set_ylabel("Peak RAM use (Gigabytes)")
ax_simupop.set_title("simuPOP with ancestry tracking")
ax_simupop.set_xlabel('Scaled recmbination rate (' + r'$\rho = 4Nr$)')
ax_simupop.set_xticks([1e3, 1e4, 1e5])
# ax.set_yscale("log")
# plt.legend(bbox_to_anchor=(1.05, 1), loc=2)
plt.tight_layout()
plt.savefig("quickfig_mem.png")
