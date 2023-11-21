import pygame
import sys

def dibujar_imagen_circular(screen, img, img_pos):
    # Crear una máscara circular
    mask = pygame.Surface((100, 100), pygame.SRCALPHA)
    pygame.draw.circle(mask, (255, 255, 255, 255), (50, 50), 50)

    # Limpiar la pantalla
    #screen.fill((255, 255, 255))

    # Dibujar la imagen en la pantalla con la máscara circular
    screen.blit(img, img_pos, special_flags=pygame.BLEND_RGBA_MULT)
    screen.blit(mask, img_pos, special_flags=pygame.BLEND_RGBA_MULT)

    # Actualizar la pantalla
    pygame.display.flip()
    

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
width, height = 500, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Imagen Circular en Pygame")

# Colores
white = (255, 255, 255)

# Cargar la imagen
image_path = "./profile_photos/1.png"  # Cambia esto a la ruta de tu imagen
img = pygame.image.load(image_path)
img = pygame.transform.scale(img, (100, 100))  # Ajusta el tamaño según sea necesario

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Llamar a la función para dibujar la imagen circular
    dibujar_imagen_circular(screen, img, (200, 200))
