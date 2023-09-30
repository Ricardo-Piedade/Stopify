from __future__ import unicode_literals
from pytube import YouTube
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from youtube_search import YoutubeSearch
import json
import concurrent.futures
import zipfile
import shutil


SPOTIPY_REDIRECT_URI="http://localhost:8080"
SCOPE = "user-top-read"


#Login with my SPOTIFY CLIENTID and CLIENT SECRET



def getTrackIDs(playlist_id):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=SCOPE))
    useridUnformated = sp.playlist(playlist_id)
    user= useridUnformated['owner']['id']
    track_ids = []
    track_names = []
    urls = []
    threads = []
    limit = 100 

    def get_tracks(offset):
        playlist = sp.user_playlist_tracks(user, playlist_id, offset=offset, limit=limit)
        return [item['track']['id'] for item in playlist['items']]

    total_tracks = sp.user_playlist_tracks(user, playlist_id)['total']

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_tracks, offset) for offset in range(0, total_tracks, limit)]

        for future in concurrent.futures.as_completed(futures):
            track_ids.extend(future.result())
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for item in track_ids:
            track_info = sp.track(item)
            strQueryYTName = track_info['name'].strip('"')
            strQueryYTArtst = track_info['artists'][0]['name'].rstrip('"')
            track_names.append(strQueryYTArtst + " - " + strQueryYTName)
        for song in track_names:
            futures = [executor.submit(SearchYoutube, song) for song in track_names]

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                urls.append(result)
    DownloadServerToZip(urls)
    

def SearchYoutube(querry):
    results = YoutubeSearch(querry, max_results=2).to_dict()
    VidURL=results[0]["url_suffix"]
    return VidURL


def DownloadServerToZip(urls):
    
    directory = os.path.dirname(os.path.abspath(__file__))
    for url in urls:
        try:
            yt = YouTube("http://www.youtube.com" + url)
            audio_stream = yt.streams.filter(only_audio=True).first()  
            audio_stream.download(output_path=directory+"\\TEMP")
        except:
            "Age Restriction"
    with zipfile.ZipFile(directory+"/output.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory+"\\TEMP"):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, directory+"\\TEMP")
                zipf.write(file_path, arcname=arcname)
    shutil.rmtree(directory+"/TEMP")
    