#!/bin/bash

# 72 hour run limit
SECONDS_TO_KILL=`echo "72*60*60"|bc -l`

for N in 1000 10000 50000
do
    KILL=0
    for size in 1000 10000 100000
    do
        if [ $KILL == 0 ]
        then
            #We will arbitrarily GC every 0.1N generations
            GC=`echo "0.1*$N"|bc -l| sed 's/\.0//'`
            GC=1000
            TIME_MEM_FILE=time_arg.N$N"."size$size".out"
            DETAILED_TIME_FILE=simupop_detailed_time_arg.N$N"."size$size".out.gz"
            /usr/bin/time -f "%e %M" -o $TIME_MEM_FILE parallel --timeout $SECONDS_TO_KILL python benchmark-simuPOP.py --popsize $N --theta $size --rho $size --nsam 100 --pdel 0.01 --gc $GC --outfile1 $DETAILED_TIME_FILE --seed ::: 42
            # --seed 43 --nsam 10 --pdel 0.1 --theta 1 --rho 1 -N 100 --outfile1 out.csv.gz
            #/usr/bin/time -f "%e %M" -o $TIME_MEM_FILE parallel --timeout $SECONDS_TO_KILL PYTHONPATH=../.. python ../../benchmarking.py --popsize $N --theta $size --rho $size --nsam 100 --pdel 0.01 --gc $GC --outfile1 $DETAILED_TIME_FILE --seed ::: 42 
            # If we terminated the job,
            # then the next params will
            # also take too long, and 
            # so we can skip running them
            STATUS=$?
            if [ $STATUS -gt 0 ]
            then
                echo "STATUS = " $STATUS
                KILL=1
            fi
        fi
    done
done
