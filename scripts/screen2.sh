#!/bin/bash
screen -dmS lb python3 src/main.py 8000 lb-victor
screen -dmS api-1 python3 src/main.py 9000 api-victor-1
screen -dmS api-2 python3 src/main.py 9001 api-victor-2
screen -dmS gs-1 python3 src/main.py 10000 gs-victor-1
screen -dmS gs-2 python3 src/main.py 10001 gs-victor-2