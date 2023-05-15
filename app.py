from flask import Flask, request, url_for, session, redirect
from spotipy.oauth2 import SpotifyOAuth
import time
import spotipy
import json
import pandas as pd
app = Flask(__name__)

# Set the secret key
app.secret_key = "ailsdbnaskljdn1312o3pih"
app.config['SESSION_COOKIE_NAME'] = 'Milad cookie'
TOKEN_INFO = 'token_info'

# Create Spotify OAuth object
def create_spotify_oauth():
    sp_oauth = SpotifyOAuth(
        client_id='da5408f13b3e4c93897e81d13139921c',
        client_secret='c1b98d403dde49baa69af72935776c74',
        redirect_uri='http://127.0.0.1:5000/redirect',
        scope='user-library-read user-top-read user-read-recently-played'
    )
    return(sp_oauth)

# Test
@app.route('/')
def index():
    return "Just a home page"

# 1) Login: on spotify for token code
@app.route('/login')
def login():
    session.clear()
    sp_oauth = create_spotify_oauth()
    oauth_url = sp_oauth.get_authorize_url()
    return redirect(oauth_url)

# 2) Redirect
@app.route('/redirect')
def redirect_page():
    #request -> athorization_code (a code)
    #swap this for access token
    sp_oauth = create_spotify_oauth()
    oauth_url = sp_oauth.get_authorize_url()
    session.clear()
    code = request.args.get('code')
    tokenInfo= sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = tokenInfo
    return redirect('http://127.0.0.1:5000/getTracks')
    return session[TOKEN_INFO]

#3)getTracks
@app.route('/getTracks')
def getTracks():
    try:
        token_info = get_token()
    except:
        print('user not logged in')
        redirect('http://127.0.0.1:5000/login')
    sp = spotipy.Spotify(auth = token_info['access_token'])
    items = sp.current_user_recently_played(limit=50)
    song_name = []
    artist_name = []
    played_at_list = []
    timestamp = []
    for songs in items['items']:
        song_name.append(songs["track"]["name"])
        artist_name.append(songs["track"]["album"]["artists"][0]["name"])
        played_at_list.append(songs["played_at"])
        timestamp.append(songs["played_at"][0:10])
    songsDict = {"song name": song_name,
        'artist name': artist_name,
        "played at": played_at_list,
        'timestamp': timestamp }
    return songsDict

#4)getTracks
def get_token():
    # check if there is any token data
    # check if the token is spired or not
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exeption"
    now = int(time.time())
    isExpired = token_info['expires_at'] - now < 60
    if isExpired:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

# Run the Flask application
if __name__ == '__main__':
    app.run()
