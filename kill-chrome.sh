#!/bin/bash
#
# This is just a simple script that loads the correct python enviroment
# and then loops forever restarting the tracker program if it ever exits.
#

cd /home/ubuntu/AnyFlightTracker


kill $(ps aux | grep '[c]hromium-browse' | awk '{print $2}')
