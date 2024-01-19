# absence_check.py
from mohawk import Sender
import json
import os
import requests
import datetime
from dotenv import load_dotenv

load_dotenv()

# Function to load JSON data from a file
def load_json_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Get the directory of the current .py file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load the data using the filenames from the .env file
team_ids_file = os.path.join(current_dir, os.getenv('TEAM_IDS_JSON'))

team_ids = load_json_data(team_ids_file)


def fetch_data_from_api(url, headers, method='GET', data=None):
    credentials = {
        'id': os.getenv("ABSENCE_IO_API_KEY_ID"),  # Your API Key ID
        'key': os.getenv("ABSENCE_IO_API_KEY"),  # Your API Key
        'algorithm': 'sha256'
    }
    sender = Sender(credentials, url, method, content=data, content_type='application/json')
    headers['Authorization'] = sender.request_header

    if method == 'POST':
        response = requests.post(url, headers=headers, data=data)
    elif method == 'GET':
        response = requests.get(url, headers=headers)
    else:
        return {'error': f"Invalid method: {method}"}

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request to {url} failed with status code {response.status_code} and response: {response.text}")
    return {'error': f"API call failed with status code {response.status_code}"}

def get_absences_for_day(date, team_name):
    # Validate the team name
    if team_name not in team_ids:
        return {"error": "Invalid team name"}

    team_id = team_ids[team_name]

    url = "https://app.absence.io/api/v2/absences"
    content_type = 'application/json'
    payload = {
        "skip": 0,
        "limit": 50,
        "filter": {
            "start": {"$lte": f"{date}T00:00:00.000Z"},
            "end": {"$gte": f"{date}T00:00:00.000Z"}
        },
        "relations": ["assignedToId", "reasonId", "approverId"]
    }
    content = json.dumps(payload)
    credentials = {
        'id': os.getenv("ABSENCE_IO_API_KEY_ID"),
        'key': os.getenv("ABSENCE_IO_API_KEY"),
        'algorithm': 'sha256'
    }
    sender = Sender(credentials, url, "POST", content=content, content_type=content_type)
    headers = {'Authorization': sender.request_header, 'Content-Type': content_type}
    absences_response = fetch_data_from_api(url, headers, 'POST', content)

    absences_for_team = []

    if absences_response and 'data' in absences_response:
        for absence in absences_response['data']:
            user_id = absence['assignedToId']
            user_url = f"https://app.absence.io/api/v2/users/{user_id}"
            user_data = fetch_data_from_api(user_url, headers, 'GET')
            
            if user_data and 'teamIds' in user_data and team_id in user_data['teamIds']:
                # Check if the absence is on a weekend
                for day_info in absence.get('days', []):
                    absence_date = datetime.datetime.strptime(day_info['date'], "%Y-%m-%dT%H:%M:%S.%fZ").date()
                    if absence_date.weekday() < 5:  # 0 is Monday, 6 is Sunday
                        # Check if it's a half-day absence
                        if day_info.get('value') == 0.5:
                            # Determine if it's AM or PM based on the start time
                            start_time = datetime.datetime.strptime(day_info['startTime'], "%Y-%m-%dT%H:%M:%S.%fZ").time()
                            half_day_period = "Morning" if start_time < datetime.time(12, 0) else "Afternoon"
                            absence['half_day_info'] = f"- Half Day ({half_day_period})"
                        else:
                            absence['half_day_info'] = ""

                        absence['user'] = user_data
                        absences_for_team.append(absence)
                        break  # Only consider the first non-weekend day

    return absences_for_team