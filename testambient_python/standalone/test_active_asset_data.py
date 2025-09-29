import requests

url = "https://embindexer.net/ember/api/dev/v1/info"

headers = {
    "Content-Type": "application/json"
}

body = {
    "type": "activeAssetData",
    "user": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK",
    "coin": "BTC"
}

try:
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    print("Response JSON:", response.json())
except requests.exceptions.HTTPError as http_err:
    print("HTTP error:", http_err, response.text)
except Exception as e:
    print("Error:", e)
