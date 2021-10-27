import requests
import time

while True:
    start = time.time()
    requests.get('http://localhost:10002/ping')
    end = time.time()

    # Write to log file
    with open("ping_log.csv", 'a+') as f:
        f.write(str(end-start) + "\n")

    time.sleep(0.1)