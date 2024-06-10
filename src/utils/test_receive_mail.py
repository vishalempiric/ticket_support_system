import requests
from datetime import datetime, timedelta


url = "https://api.eu.nylas.com/v3/grants/35d17b63-a914-46f0-bb5a-25cbe0e6f6db/messages"
headers = {
    "Accept": "application/json",
    "Authorization": "Bearer nyk_v0_95uvbyB3SffpPvd2MMVpEF4lE6JixKjxW9PhLkD2Hk4Y4YS5aiZlqSkXz07tguYg",
    "Content-Type": "application/json",
}

batch_size = 2
params = {"limit": batch_size}
response = requests.get(url, headers=headers, params=params)
response.raise_for_status()
messages = response.json()["data"]

while messages:
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    messages = response.json()["data"]
    if not messages:
        break
    for message in messages:
        print(f"Date: {datetime.fromtimestamp(message['date'])}")
        print(f"From: {message['from'][0]['email']}")
        print(f"Subject: {message['subject']}")
        print(f"Body: {message['body']}")
        print("=" * 50)
        received_date = message["date"]
    params["received_before"] = received_date