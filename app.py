# app.py
from flask import Flask
from dotenv import load_dotenv
from absence_notification import absence_notification

load_dotenv()

app = Flask(__name__)
app.register_blueprint(absence_notification)

if __name__ == '__main__':
    app.run(debug=True)
