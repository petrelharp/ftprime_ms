# Benchmark with simupop

Current benchmark is in `benchmark-simuPOP.py`. To setup, use `setup-simuPOP.sh`. Then run (this is `test.sh`):

```sh
python3 benchmark-simuPOP.py --seed 43 --nsam 10 --pdel 0.1 --theta 1 --rho 1 -N 100 --csvfile out.csv
```

For a larger run, try (his is `big-test.sh`):

```sh
python3 benchmark-simuPOP.py --seed 42 --nsam 10 --pdel 0.1 --theta 100 --gc 100 --rho 100 -N 1000 --logfile tmp.log --csvfile out.csv
```

For an even larger run. This only did about 1000 generations in an hour!

```sh
python3 benchmark-simuPOP.py -N 1000 --theta 1000 --rho 1000 --nsam 1000 --pdel 0.01 --seed 42 -G 1000 --csvfile out.csv
```

