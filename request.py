import requests
import json

url = "http://localhost:3000/api/forward"

payload = json.dumps({
    "data": "John Doe 2"
})
headers = {
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
