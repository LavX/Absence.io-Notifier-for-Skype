# skype_messaging.py
from skpy import Skype
import os
from dotenv import load_dotenv

load_dotenv()

def send_skype_message(group_id, message):
    skype = Skype(os.getenv("SKYPE_USERNAME"), os.getenv("SKYPE_PASSWORD"))
    try:
        chat = skype.chats.chat(group_id)
        chat.sendMsg(message)
        return True
    except Exception as e:
        print(f"Error in Skype Messaging: {e}")
        return False