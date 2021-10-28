import requests

for i in range(1, 10000):
    requests.get('http://localhost:8000/api/test')
