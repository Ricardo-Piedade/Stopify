import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
load_dotenv()
SPOTIPY_CLIENT_ID=os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET=os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI=os.getenv("SPOTIPY_REDIRECT_URI")
SCOPE = os.getenv("SCOPE")



sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=SCOPE))
results = sp.playlist("4BH4UNxbrsn99UhOKSVsCq", fields="items(track(name,href,album(name,href)))")
#results = sp.current_user_playlists()
print(results)
print(results.get("items"))