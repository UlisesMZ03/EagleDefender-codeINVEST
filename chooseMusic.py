import os 
from dotenv import load_dotenv
from spotipy import Spotify
import spotipy
import webbrowser
import pyautogui
import time
from spotipy.oauth2 import SpotifyClientCredentials

def list_music(song):
    load_dotenv()
    #CLIENT_SECRET=os.getenv('CLIENTSECRET')
   
    #CLIENT_ID=os.getenv("CLIENTID")
    CLIENT_SECRET="9e8a5157ce564105a39eb95fdf2330ca"
    CLIENT_ID="7f5a881f950c4eeca17b098bd9e62b2c"

    List_song=[]

    sp=Spotify(client_credentials_manager=SpotifyClientCredentials(CLIENT_ID,CLIENT_SECRET))

    result=sp.search(song)
    for i in range(0,len(result['tracks']['items'])):
        dato=result['tracks']['items'][i]
        List_song=[{'name_artist':dato['artists'][0]['name'], 'name_song':song , 'url': dato['uri']}] + List_song
    return List_song







