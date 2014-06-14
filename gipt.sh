#!/bin/sh
./ss.sh &
sleep 10
python gipt.py config.json
