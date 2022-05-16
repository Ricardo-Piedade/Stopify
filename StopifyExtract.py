import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
user = input("Insira Nome de Utilizador\n")
playlistURL = input("Insira URL Spotify Playlist\n")
print("\n\nExtraindo 100 Musicas da Playlist\n\n")
SPOTIPY_CLIENT_ID=config.SPOTIPY_CLIENT_ID
SPOTIPY_CLIENT_SECRET=config.SPOTIPY_CLIENT_SECRET
SPOTIPY_REDIRECT_URI="http://localhost:8080"
SCOPE = "user-top-read"

def extrack(sp,user,playlist_id):
    track_ids= []
    playlist = sp.user_playlist(user,playlist_id)
    for item in playlist['tracks']['items']:
        track=item['track']
        track_ids.append(track['id'])
    return track_ids
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=SCOPE))
track_ids= extrack(sp,user,playlistURL)
Spotify2Text= []
for item in track_ids:
    info = sp.track(item)
    #print(info['artists'][0]['name']+'-'+info['name'])
    Spotify2Text.append(info['artists'][0]['name']+'-'+info['name']+'\n')
    #f.write(info['artists'][0]['name']+'-'+info['name']+'\n')
try:
    f = open("ExtractedPlaylist.txt","at",encoding = 'utf-8')
    for item in Spotify2Text:
        f.write(item + '\n')
finally:
    f.close()

print("Done!")