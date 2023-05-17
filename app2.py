from flask import Flask, request, url_for, session, redirect
from spotipy.oauth2 import SpotifyOAuth
import time
import spotipy
import json
import csv
import pandas as pd
import datetime

app = Flask(__name__)

# Set the secret key
app.secret_key = "ailsdbnaskljdn1312o3pih"
app.config['SESSION_COOKIE_NAME'] = 'Milad cookie'
TOKEN_INFO = 'token_info'

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

# 1.1 Create Spotify OAuth object
def create_spotify_oauth():
    sp_oauth = SpotifyOAuth(
        client_id='da5408f13b3e4c93897e81d13139921c',
        client_secret='c1b98d403dde49baa69af72935776c74',
        redirect_uri='http://127.0.0.1:5000/redirect',
        scope='user-library-read user-top-read user-read-recently-played'
    )
    return(sp_oauth)

# 2) Redirect
@app.route('/redirect')
    #request -> athorization_code (a code)
    #swap this for access token
def redirect_page():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    tokenInfo= sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = tokenInfo
    return redirect('http://127.0.0.1:5000/getTracks')
    #return session[TOKEN_INFO]


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

    # Write the data to a CSV file
    filename = 'spotify_tracks.csv'
    recently_played_df = pd.DataFrame(songsDict)

    if check_if_valid_data(recently_played_df):
        checked_data = "Data valid, proceed to load stage"

    # writeTo_csv = recently_played_df.to_csv(filename, index=0)
#Check for valid data
def check_if_valid_data(df):
   #check if dataframe is empty
   if df.empty:
       print("No songs downloaded. Finishing the execution")
       return False
   
#    #Primary Key Check:
#    if pd.Series(df["played at"]).is_unique():
#        pass
#    else:
#        raise Exception("Primary key check is violated")
   
   #check for the null values
   if df.isnull().values.any():
       raise Exception("Null value found")
   
#    #check that all timestamps are of yesterday's songs date
#    yesterday = datetime.datetime.now() - datetime.datetime(day = 1)
#    yesterday = yesterday.replace(hour =0, minute=0, second=0, microsecond=0)
#    timestamps = df['timestamp'].tolist()
#    for timestamp in timestamps:
#        if datetime.datetime.strptime(timestamp, "%Y-%m-%d") != yesterday: #string parse time,convert a string representing a date or time into a datetime object.
#            raise Exception("at leaset one of returned songs not for yesterday")
       
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
