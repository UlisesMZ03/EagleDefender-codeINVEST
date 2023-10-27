import spotipy
import spotipy.util as util
import time

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
        duration_sec = duration_ms / 1000

        # Espera hasta que falte aproximadamente 1 segundo para que la canción termine
        time.sleep(duration_sec - 1)

        print("Aproximadamente 1 segundo para que la canción termine")
        play_song2("COLOGNE")

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


        track_info = sp.track(track_uri)
        duration_ms = track_info["duration_ms"]

        time.sleep((duration_ms / 1000) - 0.5)

        # Imprime el mensaje de que la canción está a punto de terminar
        print("Termina el juego")

        # Detén la reproducción
        sp.pause_playback()

# Ejemplo de cómo llamar a la función play_song
#play_song("GO TELLL IT TO THE MOUNTAIN") ejemploooooo 
