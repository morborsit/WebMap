#!/bin/bash

# this is an experimental function
# please, use a master branch in order to use it
exit 0

while true; do
	python3 /opt/nmapdashboard/nmapreport/nmap/cron.py &&
	echo "[SLEEP] for a while..."
	sleep 10
done
