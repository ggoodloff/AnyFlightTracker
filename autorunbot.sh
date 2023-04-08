#!/bin/bash

cd /home/ubuntu/AnyFlightTracker


echo "Killing any old sessions"

/home/ubuntu/AnyFlightTracker/stopbot.sh >/dev/null 2>&1

sleep 5

echo "Starting Tracking Bot"

# Set nohup to 1 to write to nohup
nohup=1



if [[ -f /home/ubuntu/AnyFlightTracker/nohup.out ]]
then 

    rm /home/ubuntu/AnyFlightTracker/nohup.out
fi

if [ $nohup == 1 ]
then
rm /home/ubuntu/AnyFlightTracker/__pycache__/*
    nohup /home/ubuntu/AnyFlightTracker/run_tracker.sh &
sleep 2
#tail -f /home/ubuntu/AnyFlightTracker/nohup.out
echo "############################  Bot Started ##############################"
else
rm /home/ubuntu/AnyFlightTracker/__pycache__/*
    nohup /home/ubuntu/AnyFlightTracker/run_tracker.sh </dev/null >/dev/null 2>&1 &
fi
