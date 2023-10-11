import os 
from dotenv import load_dotenv
from spotipy import Spotify
import spotipy
import webbrowser
import pyautogui
import time
from spotipy.oauth2 import SpotifyClientCredentials
import pygame
import dbus


song="In Too Deep"
author="sum 41"




#filter
#logica para agregar 1 0 3 canciones

#retorna las canciones 

def list_music(song):
    load_dotenv()
    CLIENT_SECRET=os.getenv('CLIENTSECRET')
    CLIENT_ID=os.getenv("CLIENTID")
    List_song=[]
    sp=Spotify(client_credentials_manager=SpotifyClientCredentials(CLIENT_ID,CLIENT_SECRET))
    result=sp.search(song)
    print(f'busqueda {result}')
    for i in range(0,len(result['tracks']['items'])):
        dato=result['tracks']['items'][i]
        List_song=[{'name_artist':dato['artists'][0]['name'], 'name_song':song , 'url': dato['uri']}] + List_song
    return List_song


  


