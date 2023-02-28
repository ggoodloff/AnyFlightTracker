#!/bin/bash
#
# This is just a simple script that loads the correct python enviroment
# and then loops forever restarting the tracker program if it ever exits.
#

cd /home/tracker/AnyFlightTracker

tail -f nohup.out
