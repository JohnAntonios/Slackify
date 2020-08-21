from time import time, sleep

from pathlib import Path
from dotenv import load_dotenv, set_key
from os import getenv

from slack import WebClient
from slack.errors import SlackApiError
from json import dumps

from tekore.scope import every
from tekore.util import prompt_for_user_token, refresh_user_token
from tekore import Spotify
from tekore.sender import PersistentSender

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

redirect_uri = 'http://localhost/oauth_code'
spotify_client_id = getenv("SPOTIFY_CLIENT_ID")
spotify_client_secret = getenv("SPOTIFY_CLIENT_SECRET")
spotify_refresh_token = getenv("SPOTIFY_CURRENT_USER_TOKEN")

token = None

if spotify_refresh_token:
	token = refresh_user_token(
		spotify_client_id, 
		spotify_client_secret, 
		spotify_refresh_token
	)
else:
	# This only needs to be done once, or when you would like to switch the Spotify user to connect to.
	token = prompt_for_user_token(
		spotify_client_id,
		spotify_client_secret,
		redirect_uri,
		every
	)
	set_key(env_path, "SPOTIFY_CURRENT_USER_TOKEN", token.refresh_token, "n")

spotify = Spotify(token, sender=PersistentSender())

def set_status_message(spotifyInst):
	track = spotifyInst.playback_currently_playing()
	if track is None:
		return False
	
	if track.is_playing == False:
		return False

	track_name = track.item.name
	track_artists = ', '.join([artist.name for artist in track.item.artists])

	message = f"'{track.item.name}' - {track_artists} github.com/JohnAntonios/slackthespot"

	# Slack has a limit of 100 characters for the status message.
	if len(message) > 100:
		# Omitting the artist names
		message = f"'{track.item.name}' github.com/JohnAntonios/slackthespot"

		# Remove the github link, if message is still to long
		if len(message) > 100:
			message = track.item.name

	# If its still too long, then rip
	if len(message) > 100:
		message = "The current song is too long to show in Slack"

	return message

slack_token = input("Slack Token: ")
client = WebClient(token=slack_token)

def do_it():
	print("Keep this terminal window open!")
	status_message = set_status_message(spotify)
	if status_message != False:
		try:
			new_status = dumps({
				"status_text": status_message,
				"status_emoji": ":musical_note:"
			})		
			res = client.users_profile_set(profile=new_status)
			if res.status_code == 200 or res is not None:
				print(f"Success! {status_message}")

		except SlackApiError as e:
			print("something broke")
	else:
		print("Not playing anything on Spotify or Paused or Buffering a track")

start_time = time()

while True:
	do_it()
	sleep(60.0 - ((time() - start_time) % 60.0))