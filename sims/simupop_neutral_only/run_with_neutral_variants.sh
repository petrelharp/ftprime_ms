#!/bin/bash

# 2 hour run limit
SECONDS_TO_KILL=`echo "72*60*60"|bc -l`

for N in 1000
do
    KILL=0
    for size in 1000 2500 5000 7500 10000
    do
        if [ $KILL == 0 ]
        then
            GC=1000
            TIME_MEM_FILE=time_neutral_all_neutral.N$N"."size$size".out"
            DETAILED_TIME_FILE=simupop_detailed_time_neutral_all_neutral.N$N"."size$size".out.gz"
            LOG_FILE=simupop_log_neutral_all_neutral.N$N"."size$size".log"
            /usr/bin/time -f "%e %M" -o $TIME_MEM_FILE parallel --timeout $SECONDS_TO_KILL python ../benchmark-simuPOP.py --popsize $N --theta $size --rho $size --nsam 100 --pdel 0.0 --gc $GC --outfile1 $DETAILED_TIME_FILE --logfile $LOG_FILE --record-neutral --seed ::: 42
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
