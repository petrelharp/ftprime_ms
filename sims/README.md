# Benchmark with simupop

Current benchmark is in `benchmark-simuPOP.py`. To setup, use `setup-simuPOP.sh`. Then run (this is `test.sh`):

```sh
python3 benchmark-simuPOP.py --seed 43 --nsam 10 --pdel 0.1 --theta 1 --rho 1 -N 100 --csvfile out.csv
```

For a larger run, try (his is `big-test.sh`):

```sh
python3 benchmark-simuPOP.py --seed 42 --nsam 10 --pdel 0.1 --theta 100 --gc 100 --rho 100 -N 1000 --logfile tmp.log --csvfile out.csv
```

