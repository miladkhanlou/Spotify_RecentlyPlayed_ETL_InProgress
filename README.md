# Spotify Recently Played Tracks App

This Flask web application integrates with the **Spotify API** to retrieve the user's recently played tracks and export the data to a CSV file. The app uses OAuth for authentication and interacts with Spotify using the **Spotipy** library.

## Features:
1. **User Authentication via Spotify OAuth**: Allows users to log in with their Spotify account.
2. **Recently Played Tracks**: Retrieves up to 50 of the user's recently played tracks.
3. **CSV Export**: Exports track information (song name, artist name, play time) into a CSV file.
4. **Token Refresh**: Automatically refreshes the access token when it expires.

## Technologies Used:
- **Flask**: Web framework for building the application.
- **Spotipy**: Python library for accessing the Spotify Web API.
- **OAuth 2.0**: Used for secure user authentication with Spotify.
- **CSV**: Output format for exporting recently played track data.

## How It Works:
1. **Login**: The user is directed to the Spotify login page, where they authorize the app to access their recently played tracks.
2. **Token Handling**: The app exchanges the authorization code for an access token, stores it in the session, and refreshes it when necessary.
3. **Retrieve Tracks**: The app fetches the user's recently played tracks and extracts the song names, artist names, play times, and timestamps.
4. **Export to CSV**: The track data is written to a CSV file (`spotify_recent_tracks.csv`), which can be downloaded or analyzed further.

## Setup Instructions:
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/spotify-recent-tracks.git
   cd spotify-recent-tracks
2. Install required dependencies: ```pip install -r requirements.txt```
3. Set up your Spotify Developer Account:
  * Create a Spotify Developer account and register an app to get your client_id and client_secret.
  * Set the redirect URI to http://127.0.0.1:5000/redirect in your Spotify app settings.
4.  Replace the placeholders (YOUR_CLIENT_ID, YOUR_CLIENT_SECRET, YOUR_SECRET_KEY) with your actual Spotify credentials in the app.py file.
5. Run the Flask application
6. Visit http://127.0.0.1:5000/ in your browser to start the application.

## Usage:
* Go to the /login route to authenticate with Spotify.
* After login, you'll be redirected to the /getTracks route, where your recently played tracks will be retrieved and saved as a CSV file.
* Check the root folder for the spotify_recent_tracks.csv file containing the song data.

