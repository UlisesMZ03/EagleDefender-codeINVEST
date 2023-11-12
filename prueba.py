import pygame
import sys
import os

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
width, height = 500, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Imagen Circular en Pygame")

# Colores
white = (255, 255, 255)

# Cargar la imagen
image_path = "ruta_de_tu_imagen.png"  # Cambia esto a la ruta de tu imagen
img = pygame.image.load(image_path)
img = pygame.transform.scale(img, (100, 100))  # Ajusta el tamaño según sea necesario

# Crear una máscara circular
mask = pygame.Surface((100, 100), pygame.SRCALPHA)
pygame.draw.circle(mask, (255, 255, 255, 255), (50, 50), 50)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Limpiar la pantalla
    screen.fill(white)

    # Dibujar la imagen en la pantalla con la máscara circular
    screen.blit(img, (200, 200), special_flags=pygame.BLEND_RGBA_MULT)
    screen.blit(mask, (200, 200), special_flags=pygame.BLEND_RGBA_MULT)

    # Actualizar la pantalla
    pygame.display.flip()
