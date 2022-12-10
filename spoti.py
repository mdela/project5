import os

import pandas as pd
import plotly.express as px

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

# load credentials from .env file
load_dotenv('spotify/credentials.env')

CLIENT_ID = os.getenv("CLIENT_ID", "")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")

# authenticate
client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)

# create spotify session object
session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# extract the playlist
playlist = session.user_playlist_tracks('spotify', '5GfZOIipBGtNWBwzrHWRg8') 
# get the songs
songs = playlist['items']

# create the lists
artist_name = []
track_name = []

# append every track -- along with its name and artist -- onto the lists
for i, item in enumerate(playlist['items']):
    track = item['track']
    artist_name.append(track['artists'][0]['name'])
    track_name.append(track['name'])

# loading lists into the dataframe
df = pd.DataFrame({'artist_name':artist_name,'track_name':track_name,})


# gets the number of tracks based on artist, turns it into a series
artistSeries = df['artist_name'].value_counts()
artist = artistSeries.index
numSongs = artistSeries.values

print (artist, numSongs)

# customizing the plot...
fig = px.pie(names=artist, values=numSongs)
fig.update_traces(textposition='inside', textinfo = 'value+label')


# then, plot
fig.show()