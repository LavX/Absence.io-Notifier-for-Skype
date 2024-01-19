from skpy import Skype
import os
from dotenv import load_dotenv

load_dotenv()

def list_recent_chats(username, password):
    sk = Skype(username, password)  # Connect to Skype

    chats = []
    for chat_id in sk.chats.recent():
        chat = sk.chats.chat(chat_id)  # Fetch the chat object
        chat_info = {
            "name": chat.topic if hasattr(chat, 'topic') else "Individual Chat",
            "id": chat_id
        }
        chats.append(chat_info)
    
    return chats

if __name__ == "__main__":
    skype_username = os.getenv("SKYPE_USERNAME")
    skype_password = os.getenv("SKYPE_PASSWORD")

    if skype_username and skype_password:
        recent_chats = list_recent_chats(skype_username, skype_password)
        for chat in recent_chats:
            print(f"Name: {chat['name']}, ID: {chat['id']}")
    else:
        print("Skype credentials not found. Please set SKYPE_USERNAME and SKYPE_PASSWORD environment variables.")
