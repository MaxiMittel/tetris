#!/bin/bash

python3 ../directory-service/src/main.py 7777 &

python3 ../load-balancer/src/main.py 8000 load-balancer-1 &
python3 ../load-balancer/src/main.py 8001 load-balancer-2 &

python3 ../rest-api/src/main.py 9001 api-1 &
python3 ../rest-api/src/main.py 9002 api-2 &
python3 ../rest-api/src/main.py 9003 api-3 &

python3 ../game-server/src/main.py 10001 game-server-1 &
python3 ../game-server/src/main.py 10002 game-server-2 &
python3 ../game-server/src/main.py 10003 game-server-3 &

wait