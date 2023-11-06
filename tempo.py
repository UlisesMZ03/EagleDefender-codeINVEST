import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Replace with your own client ID and client secret

def tempo():
    CLIENT_SECRET="0db3c2314d794ef28b594b4d24b07fe9"
    CLIENT_ID="8051e3ec08d240639f7cad6370e88a67"
# Authenticate with the Spotify API
    auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)

# Specify the track and artist you want to analyze
    track_name = 'hola'
    artist_name = 'GEMINI'

# Search for the track
    results = sp.search(q=f"track:{track_name} artist:{artist_name}", type='track')
    track_id = results['tracks']['items'][0]['id']

    # Get audio features for the track
    audio_features = sp.audio_features(tracks=[track_id])
    tempo = audio_features[0]['tempo']

    print(f'Tempo of the track: {tempo} BPM')

tempo()
