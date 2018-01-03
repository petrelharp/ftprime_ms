import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("gc_interval_timings.txt", sep="\t")
data['time'] /= (60. * 60.)
data['mem'] /= (1024. * 1024.)

gs = matplotlib.gridspec.GridSpec(1, 2)

ax0 = plt.subplot(gs[0])
ax1 = plt.subplot(gs[1])
ax1.yaxis.tick_right()


N1000 = data[data['N'] == 1000]

N1000g = N1000.groupby('GC')

X = 0
for n, g in N1000g:
    print(g)
    ax0.plot(g['size'], g['time'], marker='.', ms=10,
             label=r'{}'.format(g['GC'].unique()[0]))
    X += 1


N10000 = data[data['N'] == 10000]

N10000g = N10000.groupby('GC')

for n, g in N10000g:
    ax1.plot(g['size'], g['time'], marker='.', ms=10)

ax0.legend(loc='upper left', frameon=False,
           title="Simplification interval\n(generations)", fontsize='xx-small')
for ax in [ax0, ax1]:
    print(sorted(data['size'].unique()))
    ax.xaxis.set_ticks(sorted(data['size'].unique()))
    ax.set_xscale('log')
    ax.set_xlim((500, 100000))
    ax.set_xlabel(r'Region size ($\rho$ = 4Nr)')
    ax.set_ylabel("Run time (hours)")


ax0.set_title("N = 1,000", fontsize='medium')
ax1.set_title("N = 10,000", fontsize='medium')
ax1.yaxis.set_label_position("right")
plt.tight_layout()

plt.savefig("GCtime.pdf")

plt.figure()

gs = matplotlib.gridspec.GridSpec(1, 2)

ax0 = plt.subplot(gs[0])
ax1 = plt.subplot(gs[1])
ax1.yaxis.tick_right()


N1000 = data[data['N'] == 1000]

N1000g = N1000.groupby('GC')

X = 0
for n, g in N1000g:
    print(g)
    ax0.plot(g['size'], g['mem'], marker='.', ms = 10,
             label=r'{}'.format(g['GC'].unique()[0]))
    X += 1


N10000 = data[data['N'] == 10000]

N10000g = N10000.groupby('GC')

for n, g in N10000g:
    ax1.plot(g['size'], g['mem'], marker='.', ms = 10)

ax0.legend(loc="upper left", frameon=False,
           title="Simplification\ninterval (generations)", fontsize='xx-small')
for ax in [ax0, ax1]:
    print(sorted(data['size'].unique()))
    ax.xaxis.set_ticks(sorted(data['size'].unique()))
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim((500, 100000))
    ax.set_xlabel(r'Region size ($\rho$ = 4Nr)')
    ax.set_ylabel("Peak RAM use (GB)")


ax0.set_title("N = 1,000", fontsize='medium')
ax1.set_title("N = 10,000", fontsize='medium')
ax1.yaxis.set_label_position("right")
plt.tight_layout()

plt.savefig("GCmem.pdf")
