![](https://img.shields.io/badge/python-3.11-green) ![](https://img.shields.io/badge/aiogram-3.0.0b7-blue) ![](https://img.shields.io/badge/database-Redis-red)


# Universal Video Downloader Bot
![App Screenshot](https://i.imgur.com/yYwntz4.png)

## Environment Variables
To run this project, you will need to add the following environment variables to your .env file

`TOKEN`- Telegram BOT Token

`SITEURL` - Hosting\ngrok URL 

`APPHOST` - IP for listening (defaults to '127.0.0.1' if not provided)

`APPPORT` - Port for listening. For deploy it`s taken auto from host provider (defaults to 8081 if not provided)
## Run Locally (polling)
Install Redis-server

Clone the project
```bash
  git clone https://github.com/Cyero/uvdbot.git
```

Go to the project directory

```bash
  cd uvdbot
```

Install dependencies

```bash
  pip3 install -r requirements.txt
```

Install environment variables

```bash
  export TOKEN='YOUR_TOKEN_HERE'
```

Run a bot

```bash
  python3 start_polling.py
 ```


## Deployment (webhook)
Install Redis-server

Clone the project
```bash
git clone https://github.com/Cyero/uvdbot.git
```
Go to the project directory
```bash
cd uvdbot
```
Create a virtual environment
```bash
python3 -m venv env
```
Activate virtual environment
```bash
source env/bin/Activate
```
Install dependencies
```bash
pip3 install -r requirements.txt
```
Deactivate virtual environment
```bash
deactivate
```
Add rule in firewall
```bash
sudo ufw allow 443, 8081
```
Add route to your nging configuration
```bash
location /$TOKEN {
      proxy_set_header Host $http_host;
      proxy_redirect off;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Scheme $scheme;
      proxy_pass http://127.0.0.1:8081/$TOKEN;
  }
```
Make script for runnig bot as service
```bash
sudo nano /etc/systemd/system/uvdbot.service
```
Paste next code to file. 
```bash
[Unit]
Description=UVDBot
After=multi-user.target
[Service]
User=USERNAME
Environment="SITEURL=YOUR_SITE_URL"
Environment="TOKEN=YOUR_BOT_TOKEN"
Type=simple
Restart=always
WorkingDirectory=/home/USERNAME/uvdbot
ExecStart=/bin/bash -c 'cd /home/USERNAME/uvdbot/ && source env/bin/activate && python start_webhook.py'
[Install]
WantedBy=multi-user.target
```
Reload systemctl
```bash
sudo systemctl daemon-reload
```
Enable autorun
```bash
sudo systemctl enable uvdbot.service
```
Start service
```bash
sudo systemctl start uvdbot.service
``````

