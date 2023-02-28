#!/bin/bash

cd /home/tracker/AnyFlightTracker


echo "Killing any old sessions"

/home/tracker/AnyFlightTracker/stopbot.sh >/dev/null 2>&1

sleep 5

echo "Starting Tracking Bot"

# Set nohup to 1 to write to nohup
nohup=1



if [[ -f /home/tracker/AnyFlightTracker/nohup.out ]]
then 

    rm /home/tracker/AnyFlightTracker/nohup.out
fi

if [ $nohup == 1 ]
then
rm /home/tracker/AnyFlightTracker/__pycache__/*
    nohup /home/tracker/AnyFlightTracker/run_tracker.sh &
sleep 2
tail -f /home/tracker/AnyFlightTracker/nohup.out
else
rm /home/tracker/AnyFlightTracker/__pycache__/*
    nohup /home/tracker/AnyFlightTracker/run_tracker.sh </dev/null >/dev/null 2>&1 &
fi
