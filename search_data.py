import requests
import json

# Define the URL of the Flask API endpoint
url = "http://127.0.0.1:5000/execute"


data = {
    "command": "input_id",
    "params": {
        "text":"Πειραιάς, Ελλάδα",
        "method":"css_selector",
        "selector": 'input[placeholder="Περιοχή"]'
    }
}


# Define the headers for the request (Content-Type set to JSON)
headers = {
    "Content-Type": "application/json"
}

# Send the POST request to the Flask API
response = requests.post(url, headers=headers, data=json.dumps(data))

# Print the response from the server
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")



data = {
    "command": "click",
    "params": {
        "method":"xpath",
        "selector": '//*[@id="g-search-bar"]/button'
    }
}


# Define the headers for the request (Content-Type set to JSON)
headers = {
    "Content-Type": "application/json"
}

# Send the POST request to the Flask API
response = requests.post(url, headers=headers, data=json.dumps(data))

# Print the response from the server
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")