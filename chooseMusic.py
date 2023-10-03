from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import time
import pygame
import pprint
load_dotenv()
client_id = os.getenv("CLIENTID")
client_secret = os.getenv("CLIENTSECRET")



client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

pygame.mixer.init()
name='justin bieber'.upper()
song = "STAY"
results = sp.search(q=song, type='track', limit=2)


def searchSon():
  if results['tracks']['items']:
    print("cancion si encontrada")
    track = results['tracks']['items'][0]
    track_name = track['name']
    track_preview_url = track['preview_url']
    print(track_preview_url)
    if track_preview_url:
        print(f'Reproduciendo: {track_name}')
        pygame.mixer.music.load(track_preview_url)
        pygame.mixer.music.play()
        
        # Mantén el programa en ejecución mientras se reproduce la canción
        while pygame.mixer.music.get_busy():
            time.sleep(1)
        else:
            print('La canción no tiene una vista previa disponible.')
    else:
        print('Canción no encontrada.')

# Detén la reproducción de audio al final
pygame.mixer.music.stop()
pygame.mixer.quit()  
"""


print(results)
"""