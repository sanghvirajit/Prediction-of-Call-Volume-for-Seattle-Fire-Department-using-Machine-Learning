import requests

url = 'http://localhost:9696/predict'

input_ = {
    'date': '2022-01-01'
}

response = requests.post(url, json=input_).json()
print(response)