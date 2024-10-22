from flask import Flask, request, url_for, session, redirect
from spotipy.oauth2 import SpotifyOAuth
import time
import spotipy
import csv

app = Flask(__name__)

# Set secret key and session configuration
app.secret_key = "YOUR_SECRET_KEY"  # Replace with your own secret key
app.config['SESSION_COOKIE_NAME'] = 'SpotifyCookie'
TOKEN_INFO = 'token_info'

# Create a Spotify OAuth object with the necessary credentials and scopes
def create_spotify_oauth():
    return SpotifyOAuth(
        client_id='YOUR_CLIENT_ID',
        client_secret='YOUR_CLIENT_SECRET',
        redirect_uri='http://127.0.0.1:5000/redirect',
        scope='user-library-read user-top-read user-read-recently-played'
    )

# Home route
@app.route('/')
def index():
    return "Welcome to the Spotify Recent Tracks App!"

# 1) Spotify Login Route: Directs the user to Spotify for authorization
@app.route('/login')
def login():
    session.clear()  # Clear the session before a new login
    sp_oauth = create_spotify_oauth()
    authorization_url = sp_oauth.get_authorize_url()
    return redirect(authorization_url)

# 2) Redirect Route: Handles the callback from Spotify after user login
@app.route('/redirect')
def redirect_page():
    sp_oauth = create_spotify_oauth()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)  # Exchange authorization code for access token
    session[TOKEN_INFO] = token_info  # Store token info in session
    return redirect('/getTracks')  # Redirect to the getTracks route

# 3) Get Recently Played Tracks Route: Retrieves and writes recently played tracks to a CSV
@app.route('/getTracks')
def get_tracks():
    try:
        token_info = get_token()
    except Exception as e:
        print(f'Error: {e}')
        return redirect('/login')
    
    # Use Spotipy client with the access token
    sp = spotipy.Spotify(auth=token_info['access_token'])
    recent_tracks = sp.current_user_recently_played(limit=50)
    
    # Extract track data
    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []
    
    for track in recent_tracks['items']:
        song_names.append(track["track"]["name"])
        artist_names.append(track["track"]["album"]["artists"][0]["name"])
        played_at_list.append(track["played_at"])
        timestamps.append(track["played_at"][0:10])
    
    # Create a dictionary of track details
    tracks_data = {
        "Song Name": song_names,
        "Artist Name": artist_names,
        "Played At": played_at_list,
        "Timestamp": timestamps
    }
    
    # Write the track data to a CSV file
    csv_filename = 'spotify_recent_tracks.csv'
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(tracks_data.keys())  # Write column headers
        writer.writerows(zip(*tracks_data.values()))  # Write track data rows
        
    return f'Data written to CSV file: {csv_filename}'

# 4) Token Management: Retrieve or refresh token as needed
def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise Exception("User not logged in")

    # Check if the token is expired and refresh if needed
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
