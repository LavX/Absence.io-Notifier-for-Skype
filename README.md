
# 🚀 Absence.io Notifier for Skype

## 📝 Description
Absence.io Notifier is a Python Flask 🐍 application, designed to streamline notifications 📣 on Skype about team absences by integrating with Absence.io and using Skype messaging for effective communication within teams.

## 🌟 Features
- 🤖 Automated Skype notifications for team absences.
- 📅 Real-time absence data integration with Absence.io.
- 🔐 Secure API key management and authentication.
- 🖥️ User-friendly command-line interface for API key operations.

## 📋 Prerequisites
- Python 3.6 or higher.
- Flask web framework.
- An Absence.io account with API access.
- A Skype account for messaging.

## 🛠 Installation & Setup

### 📡 Clone the Repository
```bash
git clone https://github.com/yourgithubprofile/absence-notifier.git
cd absence-notifier
```

### 📦 Install Dependencies
```bash
pip install -r requirements.txt
```

### 🌐 Environment Setup
Create a `.env` file in the project root with your Absence.io API credentials and Skype credentials as per the `.env file` example provided.

## ⚙️ Configuration
- Update `team_ids.json` and `skype_groups.json` with your team's information.
- Ensure the `.env` file is correctly set up with your credentials.

## 🚀 Usage

### 🎬 Starting the Application
```bash
python app.py
```

### 🔑 API Key Management
- Add a new API key: `python app.py --add`
- Remove an API key: `python app.py --remove [key]`
- Check an API key: `python app.py --check [key]`

### 📬 Making Requests
To notify absences, send a POST request with the date:

```bash
curl -X POST http://localhost:5000/notify-absences -H 'x-api-key: YOUR_API_KEY' -H 'Content-Type: application/json' -d '{"date": "2024-01-20"}'
```

## 🗝 Obtaining Absence.io API Key
1. Sign in to your Absence.io account.
2. Navigate to 'Integrations' in your profile settings.
3. Click 'Generate API Key' and note the Key ID and the Key.
4. Use these details in the `.env` file for API integration.

## 📞 Registering a Skype Account
To use Skype notifications:
1. Go to [Skype's website](https://www.skype.com).
2. Create a new account or use an existing one.
3. Configure your Skype credentials in the `.env` file.

## 🔄 Setting Up a Cron Job for Regular Notifications
To automate the absence notifications, set up a cron job:

```bash
crontab -e
# Add the following line to run the script every day at 8 AM
0 8 * * * /usr/bin/python3 /path/to/absence-notifier/app.py >> /path/to/logfile.log 2>&1
```

## 🛠 Creating a Service on Ubuntu
To run the application as a service, create a systemd unit file:

```bash
sudo nano /etc/systemd/system/absence-notifier.service
```

Add the following content to the file:

```
[Unit]
Description=Absence Notifier Service
After=network.target

[Service]
User=username
WorkingDirectory=/path/to/absence-notifier
ExecStart=/usr/bin/python3 /path/to/absence-notifier/app.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable absence-notifier.service
sudo systemctl start absence-notifier.service
```

## 👐 Contributing
Contributions, issues, and feature requests are welcome. Feel free to check our [issues page](link_to_issues_page).

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.

## 📬 Contact
Your Name - [lavx@lavx.hu](mailto:lavx@lavx.hu)
Project Link: [https://github.com/yourgithubprofile/absence-notifier](https://github.com/yourgithubprofile/absence-notifier)
