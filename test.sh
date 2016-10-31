#!/bin/sh

RESULT=0

for i in `seq 1 3`; do
    echo "Testing M$i"
    if (./dpda.py -s M$i.txt M$i-Accept.txt); then
        echo "Accept test for M$i PASSED"
    else
        echo "Accept test for M$i FAILED"
        RESULT=1
    fi
    if (./dpda.py -s M$i.txt M$i-Reject.txt); then
        echo "Reject test for M$i PASSED"
    else
        echo "Reject test for M$i FAILED"
        RESULT=1
    fi
done

exit $RESULT
