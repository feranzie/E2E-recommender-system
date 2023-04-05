import requests

rec = '5df49b32cc709107827fb3c7'

input={
    'rec':rec
}
url = 'http://localhost:9696/predict'
response = requests.post(url, json=rec)
print(response.json())
