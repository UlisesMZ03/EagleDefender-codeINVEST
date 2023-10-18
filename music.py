import spotipy
import spotipy.util as util

SPOTIPY_CLIENT_ID = "7f5a881f950c4eeca17b098bd9e62b2c"
SPOTIPY_CLIENT_SECRET = "9e8a5157ce564105a39eb95fdf2330ca"
SPOTIPY_REDIRECT_URI = "http://localhost:8888/callback"

username = "eemmanuel698"
scope = "user-library-read user-modify-playback-state"
token = util.prompt_for_user_token(username, scope, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)

sp= spotipy.Spotify(auth=token)

song_name="runaway kanye"
results= sp.search(q=song_name, type="track", limit=1)

if results["tracks"]["items"]:
    track_uri=results["tracks"]["items"][0]["uri"]
else: 
    print("no se encontro la cancion")
    exit()


sp.start_playback(uris=[track_uri])