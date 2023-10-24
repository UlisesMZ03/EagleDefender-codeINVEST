import spotipy
import spotipy.util as util
import time
 

import conteopts


duration_sec = None
duration_sec2 = None

# (Tus datos de configuración)
SPOTIPY_CLIENT_ID = "7f5a881f950c4eeca17b098bd9e62b2c"
SPOTIPY_CLIENT_SECRET = "9e8a5157ce564105a39eb95fdf2330ca"
SPOTIPY_REDIRECT_URI = "http://localhost:8888/callback"

username = "eemmanuel698"
scope = "user-library-read user-modify-playback-state"

def play_song(song):
    token = util.prompt_for_user_token(username, scope, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)
    sp = spotipy.Spotify(auth=token)

    # Reproduce la canción recibida como argumento
    results = sp.search(q=song, type="track", limit=1)

    if results["tracks"]["items"]:
        track_uri = results["tracks"]["items"][0]["uri"]
        sp.start_playback(uris=[track_uri])
        print("Reproduciendo la canción:", song)

        # Obtenemos la duración de la canción en milisegundos
        duration_ms = results["tracks"]["items"][0]["duration_ms"]
        # Convertimos la duración a segundos
        global duration_sec
        duration_sec = duration_ms / 1000

        # Espera hasta que falte aproximadamente 1 segundo para que la canción termine
        time.sleep(duration_sec - 1)

        print("Aproximadamente 1 segundo para que la canción termine")
        
        play_song2("poor little match boy")

        defense_time(duration_sec)
        return(duration_sec)
    else:
        print("No se encontró la canción")

def play_song2(song):
    print("ENTRO EN 2")
    token = util.prompt_for_user_token(username, scope, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)
    sp = spotipy.Spotify(auth=token)

    # Reproduce la canción recibida como argumento
    results = sp.search(q=song, type="track", limit=1)

    if results["tracks"]["items"]:
        track_uri = results["tracks"]["items"][0]["uri"]
        sp.start_playback(uris=[track_uri])
        print("Reproduciendo la canción:", song)


        duration_ms2 = results["tracks"]["items"][0]["duration_ms"]
        # Convertimos la duración a segundos
        global duration_sec2
        duration_sec2 = duration_ms2 / 1000

        # Espera hasta que falte aproximadamente 1 segundo para que la canción termine
        time.sleep(duration_sec2 - 1)

        print("Aproximadamente 1 segundo para que la canción termine")
        

        attack_time(duration_sec2)
        return(duration_sec2)
    

def attack_time(duration):
    print (duration)
    return(duration)

def defense_time(durationt):
    print (durationt)
    return(durationt)

# Ejemplo de cómo llamar a la función play_song
play_song("GO TELLL IT TO THE MOUNTAIN")

print("Duración de la canción 1:", duration_sec)
print("Duración de la canción 2:", duration_sec2)



