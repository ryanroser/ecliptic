#!/bin/bash

# This script starts the Celery ecliptic workers, Flower, and the Celery scheduled tasks

# start celery workers
celery -A ecliptic worker -l info -c 2 &>> logs/celery_workers.log &

# start flower
celery flower -A ecliptic -l info &>> logs/celery_flower.log &

# start celery scheduled tasks (optional)
celery beat -A ecliptic &>> logs/celery_beat.log &
