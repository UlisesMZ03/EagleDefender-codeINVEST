from PIL import Image
import sys
import pygame

# Abre una imagen

# Puedes mostrar la imagen si lo deseas



def getImg():
    imagen = Image.open("./profile_photos/38.png")
    imagen.show()

def load_selected_image(image_path):
    if os.path.exists(image_path):
        image_surface = pygame.image.load(image_path).convert()
        return pygame.transform.scale(image_surface, (camera_preview_rect.width, camera_preview_rect.height))
    return None