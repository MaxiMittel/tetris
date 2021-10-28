#!/bin/bash

screen -dmS directory cd ../directory-service && python3 src/main.py 7777
screen -dmS webserver cd ../webserver && python3 src/main.py
screen -dmS lb cd ../load-balancer && python3 src/main.py 8000 lb-maxi
screen -dmS api-1 cd ../rest-api && python3 src/main.py 9000 api-maxi-1
screen -dmS api-2 cd ../rest-api && python3 src/main.py 9001 api-maxi-2
screen -dmS gs-1 cd ../game-server && python3 src/main.py 10000 gs-maxi-1
screen -dmS gs-2 cd ../game-server && python3 src/main.py 10001 gs-maxi-2