#!/bin/bash

# 72 hour run limit
SECONDS_TO_KILL=`echo "72*60*60"|bc -l`

for N in 1000 10000 
do
    for size in 1000 2500 5000 7500 10000 15000
    do
        #We will arbitrarily GC every 0.1N generations
        GC=`echo "0.1*$N"|bc -l| sed 's/\.0//'`
        GC=1000
        TIME_MEM_FILE=time_arg_all_neutral.N$N"."size$size".out"
        DETAILED_TIME_FILE=detailed_time_arg_all_neutral.N$N"."size$size".out.gz"
        /usr/bin/time -f "%e %M" -o $TIME_MEM_FILE parallel --timeout $SECONDS_TO_KILL PYTHONPATH=../.. python ../../benchmarking.py --popsize $N --theta $size --rho $size --nsam 100 --pdel 0.0 --gc $GC --outfile1 $DETAILED_TIME_FILE --seed ::: 42 
    done
done
