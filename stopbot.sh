#!/bin/bash
#
# This is just a simple script that loads the correct python enviroment
# and then loops forever restarting the tracker program if it ever exits.
#

cd /home/ubuntu/AnyFlightTracker

kill $(ps aux | grep '[t]racker.py' | awk '{print $2}')
kill $(ps aux | grep '[r]un_tracker.sh' | awk '{print $2}')
kill $(ps aux | grep '[c]hromedriver' | awk '{print $2}')
kill $(ps aux | grep '[c]hromium-browse' | awk '{print $2}')


echo "Clearing chrome cache directory"
rm -rf /home/ubuntu/AnyFlightTracker/chromium/*
rm -rf /home/ubuntu/AnyFlightTracker/chromium/.*

