import requests

url = 'http://localhost:9696/predict'

input_ = {
    'datetime': '2022-01-01 15:00:00'
}

response = requests.post(url, json=input_).json()
print(response)