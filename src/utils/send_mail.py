import json
from dotenv import load_dotenv
load_dotenv()

import os
import sys
from nylas import Client


nylas = Client(
    os.environ.get('NYLAS_API_KEY'),
    os.environ.get('NYLAS_API_URI')
)

grant_id = os.environ.get("NYLAS_GRANT_ID")
email = os.environ.get("EMAIL")

# message = nylas.messages.send(
#   grant_id,
#   request_body={
#     "to": [{ "name": "Name", "email": "vishalprajapati22052001@gmail.com" }],
#     "reply_to": [{ "name": "Name", "email": "vishalprajapati22052001@gmail.com" }],
#     "subject": "subject",   
#     "body": "body",
#   }
# )

# print(message)

messages = nylas.messages.list(
  grant_id,
  query_params={
    "limit": 5,
    # "received_after":1717396910,
  }
)

print("====message===== ",messages)