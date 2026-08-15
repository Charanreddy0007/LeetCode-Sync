#!/bin/bash

totaltime=0

for i in {1..19}
do
    start=$(date +%s.%N)

    python main.py

    end=$(date +%s.%N)

    duration=$(echo "$end - $start" | bc)

    totaltime=$(echo "$totaltime + $duration" | bc)

    echo "-----------------------"
    echo "Total Time: ${duration} s"
    echo "-----------------------"
done

avg=$(echo "scale=6; $totaltime / 19" | bc)

echo "Avg time: $avg s"
