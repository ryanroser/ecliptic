#!/bin/bash

# stops the celery workers, flower, and beat processes that mention ecliptic
for x in $(ps axjf | grep -E '^\s+1.*celery.*ecliptic' | sed 's/  */ /g' | cut -d' ' -f3) 
do
	echo Killing PID $x...
	kill $x
	echo done
done
