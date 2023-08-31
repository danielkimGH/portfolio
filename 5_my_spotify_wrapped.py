import gspread
import time
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth
from datetime import date

def getTrackIDs(time_frame):
    """Returns list of track IDs"""
    track_ids = []

    for song in time_frame['items']:
        track_ids.append(song['id'])

    return track_ids


def getTrackFeatures(id):
    """Returns list of track features"""
    meta = sp.track(id)

    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    spotify_url = meta['external_urls']['spotify']
    album_cover = meta['album']['images'][0]['url']
    track_info = [name, album, artist, spotify_url, album_cover]
    return track_info


def convertToDF(track_ids, time_range):
    """Converts to track features to a dataframe and saves """
    tracks = []

    for i in range(len(track_ids)):
        time.sleep(0.5)
        track = getTrackFeatures(track_ids[i])
        tracks.append(track)

    df = pd.DataFrame(tracks, columns=['name', 'album', 'artist', 'spotify_url', 'album_cover'])
    df.to_csv(f'{date.today()}-{time_range}.csv')


def insertToGsheet(track_ids, time_period):
    """Insert track dataframe into Google spreadsheet"""
    tracks = []

    for i in range(len(track_ids)):
        time.sleep(0.5)
        track = getTrackFeatures(track_ids[i])
        tracks.append(track)

    df = pd.DataFrame(tracks, columns=['name', 'album', 'artist', 'spotify_url', 'album_cover'])
    gc = gspread.service_account(filename='my-spotify-wrapped-test-397420-fa0ac2b01211.json')
    sh = gc.open('My Spotify Wrapped')
    worksheet = sh.worksheet(f'{time_period}')
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

    print(f'{time_period} tracks done')


# Read in Spotify client credentials
with open('spotify_client.txt') as file:
    data = file.read().splitlines()

c_ID, c_secret = data[0], data[1]

SPOTIPY_CLIENT_ID = c_ID
SPOTIPY_CLIENT_SECRET = c_secret
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:9090'
SCOPE = "user-top-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=SCOPE))

time_ranges = ['short_term', 'medium_term', 'long_term']

for time_period in time_ranges:
    top_tracks = sp.current_user_top_tracks(limit=20, offset=0, time_range=time_period)
    track_ids = getTrackIDs(top_tracks)
    insertToGsheet(track_ids, time_period)
