from __future__ import unicode_literals
import youtube_dl
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from youtube_search import YoutubeSearch
from tkinter import Tk, filedialog
import os

SPOTIPY_CLIENT_ID="get your own at Spotify API"
SPOTIPY_CLIENT_SECRET="get your own at Spotify API"
SPOTIPY_REDIRECT_URI="http://localhost:8080"
SCOPE = "user-top-read"

def getTrackIDs(sp,user, playlist_id):
    track_ids= []
    playlist = sp.user_playlist(user,playlist_id)
    for item in playlist['tracks']['items']:
        track = item['track']
        track_ids.append(track['id'])
    return track_ids

def SearchYoutube(querry):
    results = YoutubeSearch(querry, max_results=10).to_dict()
    VidURL=results[0]["url_suffix"]
    return VidURL

def pathChooser():
    root = Tk()
    root.withdraw()
    root.attributes('-topmost',True)
    path = filedialog.askdirectory()
    return path

def getURL(sp,track_ids):
    PlayListURL=[]
    print(len(track_ids))
    for item in track_ids:
        trackinf=sp.track(item)
        strQueryYTName = trackinf['name'].strip('"')
        strQueryYTArtst = trackinf['artists'][0]['name'].rstrip('"')
        #print('ARTIST:%s'%trackinf['name'])
        #print('TYPE:'+str(type(strQueryYTName)))
        querryYT = strQueryYTArtst + " " + strQueryYTName
        urlVid=SearchYoutube(querryYT)
        print(querryYT," ",urlVid)
        PlayListURL.append(urlVid)
    return PlayListURL

def getFile(listURL,path):
    ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320'
            }],
            'postprocessor_args': [
                '-ar', '16000'
            ],
            'prefer_ffmpeg': True,
            'keepvideo': False   
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        for item in listURL:
            ydl.download(["http://www.youtube.com"+item])
            
            
       

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=SCOPE))
track_ids= getTrackIDs(sp,'Ricardo Piedade','0prorsAY9oH8fkkJQFhWhA')
listURL = getURL(sp,track_ids)
print('/n')
getFile(listURL,pathChooser())


    




