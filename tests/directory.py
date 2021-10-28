import requests
import time

while True:
    start = time.time()
    requests.get('http://18.192.65.75:7777/directory-service/getlb')
    end = time.time()

    # Write to log file
    with open("directory_log.csv", 'a+') as f:
        f.write(str(end-start) + "\n")