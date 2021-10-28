#!/bin/bash

screen -dmS directory python3 src/main.py 7777
screen -dmS webserver python3 src/main.py
screen -dmS lb python3 src/main.py 8000 lb-maxi
screen -dmS api-1 python3 src/main.py 9000 api-maxi-1
screen -dmS api-2 python3 src/main.py 9001 api-maxi-2
screen -dmS gs-1 python3 src/main.py 10000 gs-maxi-1
screen -dmS gs-2 python3 src/main.py 10001 gs-maxi-2