import os 
from dotenv import load_dotenv
from spotipy import Spotify
import spotipy
import webbrowser
import pyautogui
import time
from spotipy.oauth2 import SpotifyClientCredentials
import pygame
load_dotenv()


song="In Too Deep"
author="sum 41"
CLIENT_SECRET=os.getenv('CLIENTSECRET')
CLIENT_ID=os.getenv("CLIENTID")



#filter
#logica para agregar 1 0 3 canciones

#retorna las canciones 

def list_music(song):
    List_song=[]
    sp=Spotify(client_credentials_manager=SpotifyClientCredentials(CLIENT_ID,CLIENT_SECRET))
    result=sp.search(song)
    for i in range(0,len(result['tracks']['items'])):
        dato=result['tracks']['items'][i]
        List_song=[{'name_artist':dato['artists'][0]['name'], 'name_song':song , 'url': dato['uri']}] + Lista
    return List_song

song=input("ingresa la cancion")
def music(n_song):
   List_favorite_song=[]
   for event in pygame.event.get():
       if event.type==pygame.KEYDOWN:
          if len(list_music)<3:
            list_music(song)

           
           


