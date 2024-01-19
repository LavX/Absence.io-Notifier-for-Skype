# absence_notification.py
from flask import Blueprint, request, jsonify
from absence_check import get_absences_for_day
from skype_messaging import send_skype_message
from dotenv import load_dotenv
from api_key_manager import require_api_key
import json
import os

load_dotenv()

# Function to load JSON data from a file
def load_json_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Get the directory of the current .py file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load the data using the filenames from the .env file
skype_groups_file = os.path.join(current_dir, os.getenv('SKYPE_GROUPS_JSON'))

skype_groups = load_json_data(skype_groups_file)

absence_notification = Blueprint('absence_notification', __name__)

@absence_notification.route('/notify-absences', methods=['POST'])
@require_api_key
def notify_absences():
    data = request.json
    date = data.get('date')

    if not date:
        return jsonify({"error": "Missing date"}), 400

    for team_name, group_ids in skype_groups.items():
        absences_response = get_absences_for_day(date, team_name)
        
        # Handle None response before checking for "error"
        if absences_response is None:
            return jsonify({"error": f"Failed to fetch absence data for {team_name}"}), 500

        if not absences_response:
            continue  # No absences for this team, skip to the next

        message_lines = []
        for absence in absences_response:
            user_info = f"{absence.get('user', {}).get('firstName', 'Unknown')} {absence.get('user', {}).get('lastName', '')}"
            half_day_info = absence.get('half_day_info', '')
            message_lines.append(f"👤 {user_info} {half_day_info}".strip())

        if message_lines:
            message = f"🌴 People on vacation in {team_name} on {date} 🌴:\n" + "\n".join(message_lines)
            for group_id in group_ids:
                if not send_skype_message(group_id, message):
                    return jsonify({"error": f"Failed to send message to Skype group for {team_name}"}), 500

    return jsonify({"success": "Absence info posted to all Skype groups successfully"}), 200