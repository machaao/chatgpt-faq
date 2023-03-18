# AI powered FAQ Chatbot
Build your own ChatGPT powered faq / knowledge base chatbot that can infer and answer queries based on the information provided via an external data source 
## Requirements for running it locally on laptop ##

* Windows / Mac / Linux with Git installed
* Python 3.8+
* MessengerX.io API Token - FREE for Indie Developers
* Open AI Key
* Ngrok for Tunneling 

### Install requirements ###
```bash
pip install -r requirements.txt
```

### Create a new .env file in the root directory ###
* For Linux / Mac
```bash
nano -w .env
```

* For Windows
```bash
type nul > .env 
```

### Add the following values to your .env file
```bash
OPENAI_API_KEY=<YOUR_OPEN_AI_KEY> # your open ai key
MESSENGERX_BASE_URL=https://ganglia.machaao.com
OVERRIDE_INDEX_CHECK=False 
```
* Set OVERRIDE_INDEX_CHECK to ```True``` if you want the bot to automatically 
 retrain your index when you update your data source

### Run your chatbot app on your local server
```bash
python app.py
```

### Start ngrok.io tunnel in a new terminal (local development) ###
```
ngrok http 5000
```

### Update your webhook to receive messages ###
Update your bot Webhook URL at [MessengerX.io Portal](https://portal.messengerx.io) with the url provided by ngrok
```
https://<Your NGROK URL>/machaao/hook
```

* If your ```NGROK URL``` is ```https://e9fe-115-187-40-104.in.ngrok.io``` then your bot 
settings page should look like this 👇🏻
![figure](/assets/mx_bot.png)

### Your chatbot is now ready to start receiving incoming messages from users
```bash
# HappyCoding
```
