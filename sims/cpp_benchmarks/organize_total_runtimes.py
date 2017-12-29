import sys
import re
import pandas as pd
files = []

for i in sys.argv[1:]:
    OK = True
    for line in open(i, 'r'):
        if re.search('non-zero', line):
            OK = False
            break
    if OK is True:
        files.append(i)

dflist = []
for i in files:
    ARG = True
    Q = False
    SEL = True
    if re.search('all_neutral', i):
        SEL = False
        if re.search('neutral_all_neutral', i):
            ARG = False
    else:
        if re.search('with', i):
            ARG = False
        if re.search('queue', i):
            Q = True

    print(i, ARG, Q, SEL)
    d = pd.read_csv(i, sep=" ", names=['time', 'mem'], index_col=False)
    d['arg'] = [ARG]
    d['queue'] = [Q]
    d['sel'] = [SEL]
    fields = i.split('.')
    fields[1] = re.sub('N', '', fields[1])
    fields[2] = re.sub('size', '', fields[2])
    d['N'] = float(fields[1])
    d['rho'] = float(fields[2])
    dflist.append(d)

df = pd.concat(dflist)

# This is a bit loose:
df['time_per_gen'] = df.time / (10. * df.N)

df.to_csv("cpp_timings.txt", index=False, sep="\t")
