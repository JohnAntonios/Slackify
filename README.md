# Slack The Spot
Change your slack status to your currently played track on Spotify, regardless of the device!

## Getting Started

### Python shenanigans
You will need [Python >= 3.7](https://python.org) installed on your computer.

I recommend a virtual environment setup, to isolate this app from any other Python app and not have conflicting packages installed.

After installing Python, go to your terminal:

```
pip install virtualenv
cd <to your chosen folder location>
git clone https://github.com/JohnAntonios/slackthespot.git
cd slackthespot
virtualenv venv

# For Windows:
.\venv\Scripts\activate

# For Mac OS X / Linux / UNIX:
source venv/bin/activate

pip install -r requirements.txt
```

---

### API shenanigans
You will need to create a ```.env``` file in the root directory of the git folder.

In the .env file,  3 keys are required that you will need to obtain yourself:

[This sample](sample.env) file has been provided for you to follow along with.

<b>SLACK_OAUTH_ACCESS_TOKEN</b>

You will need to generate this token in [Slack API](https://api.slack.com/apps?new_app=1), simply create an App and link it to your desired workspace, then install the app, this will generate an OAUTH key for you to copy and paste. 

<b>
SPOTIFY_CLIENT_ID<br />
SPOTIFY_CLIENT_SECRET
</b>

You will need to generate these two keys in [Spotify for Developers](https://developer.spotify.com/dashboard/login).

1. Create an App
2. Fill in the details and press next.
3. Press Non-Commercial
4. Confirm to the agreements.

This will now redirect you to the dashboard of your newly created app.

Press <b>SHOW CLIENT SECRET</b> and paste both the Client ID and Client Secret into the .env file.

5. Press Edit Settings
6. In the <b>Redirect URIs</b>, add: ```http://localhost/oauth_code```
---

### Running the app

After finally getting the above shenanigans sorted, you are ready to start the app!

```
python app.py
```

For the first run, a browser will open requiring you to sign in with the Spotify account you would like to grab the currently playing track from.

After signing in, you will be redirected to ```http:/localhost/oauth_code?=...``` copy the entire URL and paste it in the terminal window.

This will save that user, so that you do not need to authenticate the user again. If you wish to sign in into a different account, simply remove the <b>SPOTIFY_CURRENT_USER_TOKEN</b> key-value from your ```.env``` file.

The app will automatically update your slack status every minute, as there is no event listener / webhook integrated in Spotify's API with Python + Tekore; so polling was implemented.

The app tracks the device that the user is logged into, so it can even update it from your Phone's Spotify!

---

## Dependencies
[tekore](https://github.com/felix-hilden/tekore)

[python-dotenv](https://github.com/theskumar/python-dotenv)

[python-slackclient](https://github.com/slackapi/python-slackclient)