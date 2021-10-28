import requests
import time

while True:
    start = time.time()
    requests.get('http://18.192.65.75:8000/sessions/list')
    end = time.time()

    # Write to log file
    with open("api_log.csv", 'a+') as f:
        f.write(str(end-start) + "\n")