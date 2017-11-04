echo "Must have fwdpy11_arg_example installed!!"
wget https://github.com/molpopgen/fwdpy11_arg_example/blob/update_to_edge/benchmarking.py
python ./benchmark-simuPOP.py --theta 10 --rho 10 --nsam 10 --pdel 0 --gc 50  \
	--outfile1 out.log.gz --seed 42 --popsize 100 --treefile
simupoptree.hdf5
python ./benchmarking.py --theta 10 --rho 10 --nsam 10 --pdel 0 --gc 50 \
	--outfile1 out.log.gz --seed 42 --popsize 100 --treefile fwdpptree.hdf5

