#!/bin/bash

# start first process
./start-gunicorn.sh -D
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start gunicorn: $status"
  exit $status
fi

# start second process
./start-celery.sh -D
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start celery: $status"
  exit $status
fi

while sleep 60; do
  ps aux | grep my_first_process | grep -q -v grep
  PROCESS_1_STATUS=$?
  ps aux | grep my_second_process | grep -q -v grep
  PROCESS_2_STATUS=$?

  if [ $PROCESS_1_STATUS -ne 0 -o $PROCESS_2_STATUS -ne 0 ]; then
    echo "One of the processes has already exited."
    exit 1
  fi
done
