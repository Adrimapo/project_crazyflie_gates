#!/bin/bash

# TODO: Add an argument to set the iterations number

for i in $(seq 1 40); do

    # Execute with -a to use 1 door
    ./launch_as2.bash -s  -a false &




    sleep 20
    touch log.txt
    python3 src/mission.py -s  > log.txt

    ./stop.bash
    rm log.txt

    sleep 20
done
