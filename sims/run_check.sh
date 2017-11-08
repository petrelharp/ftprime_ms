python ./benchmark-simuPOP.py --theta 10 --rho 10 --nsam 10 --pdel 0 --gc 50 --outfile1 /dev/null --seed 42 --popsize 100 --treefile simupoptree.hdf5
python ./check.py --rho 10 --theta 10 --popsize 100 --seed 111 -o check-10-10-100.png

python ./benchmark-simuPOP.py --theta 5 --rho 5 --nsam 10 --pdel 0 --gc 50 --outfile1 /dev/null --seed 42 --popsize 200 --treefile simupoptree.hdf5
python ./check.py --rho 5 --theta 5 --popsize 200 --seed 111 -o check-5-5-200.png

python ./benchmark-simuPOP.py --theta 20 --rho 20 --nsam 10 --pdel 0 --gc 50 --outfile1 /dev/null --seed 42 --popsize 100 --treefile simupoptree.hdf5
python ./check.py --rho 20 --theta 20 --popsize 100 --seed 111 -o check-20-20-100.png -N 500

python ./benchmark-simuPOP.py --theta 30 --rho 30 --nsam 10 --pdel 0 --gc 50 --outfile1 /dev/null --seed 42 --popsize 200 --treefile simupoptree.hdf5
python ./check.py --rho 30 --theta 30 --popsize 200 --seed 111 -o check-30-30-200.png -N 500
