# import requests
# from models import Email  # Assuming you have a SQLAlchemy Email model
# from database import db  # Assuming db is your SQLAlchemy session

# url = "https://api.eu.nylas.com/v3/grants/35d17b63-a914-46f0-bb5a-25cbe0e6f6db/messages"

# headers = {
#     "Accept": "application/json",
#     "Authorization": "Bearer nyk_v0_95uvbyB3SffpPvd2MMVpEF4lE6JixKjxW9PhLkD2Hk4Y4YS5aiZlqSkXz07tguYg",
#     "Content-Type": "application/json",
# }

# # Check if there are any emails in the database
# check_emails = db.query(Email).all()

# if not check_emails:
#     # If no emails in the database, fetch emails in batches
#     oldest_email_timestamp = None
#     page = 1
#     while True:
#         response = requests.get(url, headers=headers, params={'limit': 100, 'page': page})
#         if response.status_code == 200:
#             emails = response.json()["data"]
#             if not emails:
#                 break  # No more emails to fetch
#             # Find the oldest email in the batch
#             batch_oldest_email = min(emails, key=lambda x: x['date'])
#             if oldest_email_timestamp is None or batch_oldest_email['date'] < oldest_email_timestamp:
#                 oldest_email_timestamp = batch_oldest_email['date']
#             page += 1
#         else:
#             print(f"Failed to fetch emails. Status code: {response.status_code}")
#             print(f"Error message: {response.text}")
#             break

#     if oldest_email_timestamp:
#         print("Oldest email timestamp:", oldest_email_timestamp)
#         # Now use the oldest email timestamp to fetch newer emails
#         params = {'received_after': oldest_email_timestamp}
#     else:
#         print("No emails found.")
# else:
#     # Calculate received_after based on the timestamp of the latest processed email
#     latest_processed_email = db.query(Email).order_by(Email.created_at.desc()).first()
#     received_after = int(latest_processed_email.created_at.timestamp())
#     print("Received after timestamp:", received_after)
#     params = {'received_after': received_after}

# # Send the GET request to fetch emails based on the parameters
# response = requests.get(url, headers=headers, params=params)

# if response.status_code == 200:
#     emails = response.json()["data"]
#     if emails:
#         # Process the new emails
#         for email in emails:
#             process_email(email)  # Implement this function to process each email
#     else:
#         print("No new emails found.")
# else:
#     print(f"Failed to fetch emails. Status code: {response.status_code}")
#     print(f"Error message: {response.text}")













from datetime import datetime, timedelta


current_date = datetime.utcnow() - timedelta(microseconds=3)

received_after = int(current_date.timestamp())

print(received_after)