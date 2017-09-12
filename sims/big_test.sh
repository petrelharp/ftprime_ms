#!/bin/bash
python3 benchmark-simuPOP.py --seed 42 --nsam 10 --pdel 0.1 --theta 100 --gc 100 --rho 100 -N 1000 --logfile tmp.log --csvfile out.csv
