#!/bin/bash
#
# This is just a simple script that loads the correct python enviroment
# and then loops forever restarting the tracker program if it ever exits.
#

cd /home/tracker/AnyFlightTracker

while :
do
	echo
	echo '***** Restarting AircraftTracker ' `date --utc --rfc-3339=ns`
	echo

	python3 tracker.py

	echo
	echo '***** AircraftTracker exited ' `date --utc --rfc-3339=ns`
	echo

	sleep 5

done

