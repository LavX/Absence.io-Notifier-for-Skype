# absence_hawk_request_simulation.py
import requests
import os
from mohawk import Sender
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def generate_hawk_header(url, method, credentials, payload):
    sender = Sender(
        credentials,
        url,
        method,
        content=payload,
        content_type='application/json'
    )
    return sender.request_header

# replace 'team_id' with your actual team's ID
#team_id = '56968e30a4c5b7f74f82718b'
# url = f'https://app.absence.io/api/v2/teams/{team_id}'

# url = f'https://app.absence.io/api/v2/absences/'
url = f'https://app.absence.io/api/v2/users/646b529c104956e2e13c45ac'
# Your API Key ID and API Key for the Hawk credentials
credentials = {
    'id': os.getenv("ABSENCE_IO_API_KEY_ID"),  # Your API Key ID
    'key': os.getenv("ABSENCE_IO_API_KEY"),  # Your API Key
    'algorithm': 'sha256'
}

# Hawk payload for GET request is typically empty
payload = ''
# payload = json.dumps({
#     "skip": 0,
#     "limit": 50,
#     "filter": {  
#          "start": {"$lte" : "2015-12-28T00:00:00.000Z"},
#          "end": {"$gte": "2015-12-28T00:00:00.000Z"},     
#          "reasonId":"53ec876edf869a0200707ac5"
#     },
#     "relations": ["assignedToId", "reasonId", "approverId"]
# })

# Generate the Hawk Authorization Header
hawk_header = generate_hawk_header(url, 'GET', credentials, payload)

# Make the GET request with the Hawk header
headers = {
    'Authorization': hawk_header,
    'Content-Type': 'application/json'
}

response = requests.get(url, headers=headers)

# Debug output
print(f'Request URL: {url}')
print(f'Request method: GET')
print(f'Hawk header: {hawk_header}')
print(f'Response status code: {response.status_code}')
print(f'Response headers: {response.headers}')
print(f'Response text: {response.text}')

# Check for empty response content
if not response.content:
    print(f'Warning: The response from the server is empty.')