#!/bin/bash

while true; do
    curl http://localhost:3000/
    exitCode=$?
    if [ ${exitCode} -ne 0 ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') - FAILURE: Server not reachable. Exit Code: $exitCode" >> "./logs/health.log"
    fi

    sleep 10
done