import main
import redis
import json
import base64
import os
import requests

from dotenv import load_dotenv

load_dotenv()
twitter = main.make_token()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
token_url = "https://api.twitter.com/2/oauth2/token"

t = main.r.get('token')
bb_t = t.decode("utf8").replace("'", '"')
data = json.loads(bb_t)

refreshed_token = twitter.refresh_token(
    client_id=client_id,
    client_secret=client_secret,
    token_url=token_url,
    refresh_token=data["refresh_token"]
)

st_refreshed_token = '"{}"'.format(refreshed_token)
j_refreshed_token = json.loads(st_refreshed_token)
main.r.set('token', j_refreshed_token)

trocadilho = main.make_trocadilho()
payload = {'text': '{}'.format(trocadilho)}
main.post_tweet(payload, refreshed_token)