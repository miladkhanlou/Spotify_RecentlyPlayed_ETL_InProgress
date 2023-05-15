Here's a rundown of the code's features:

1. The code creates a Flask application, configures the secret key and session settings, and defines the TOKEN_INFO constant to store the session token information.

2. Make a SpotifyOAuth object with the required client credentials, redirect URI, and scopes.

3. The /login route starts the Spotify authentication process by directing the user to the Spotify authorization URL.

4. The callback from the Spotify authorization process is handled by the /redirect route. 
It retrieves the authorization code from the request arguments, exchanges it for an access token using the SpotifyOAuth object's get_access_token() method, and stores the token information in the session. The user is then redirected to the /getTracks route.

5. The /getTracks route uses the get_token() function to retrieve token information from the session. If the token expires, the SpotifyOAuth object's refresh_access_token() method is used to refresh the access token. It then uses the access token to create a Spotipy Spotify API client and retrieves the current user's recently played tracks. The items from the track are extracted and returned as a string.

6. The get_token() function determines whether or not token information exists in the session. If not, an exception is raised. It also checks to see if the token has expired and, if so, restores it using the SpotifyOAuth object's refresh_access_token() method. Finally, the updated token information is returned.

The / route acts as the home page, returning a simple string message.
