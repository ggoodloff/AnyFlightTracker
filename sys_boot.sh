#!/bin/bash
#
# This is just a simple script that loads the correct python enviroment
# and then loops forever restarting the tracker program if it ever exits.
#

cd /home/ubuntu/AnyFlightTracker

#	python3 tracker.py </dev/null >/dev/null 2>&1 &
	python3 tracker.py  >nohup.bootlog  2>&1 &
	sleep 5

