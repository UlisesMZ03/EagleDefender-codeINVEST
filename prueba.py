import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configurar la pantalla
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame Window")

# Cargar el icono
icon = pygame.image.load("./images/game/escIcon.png")  # Reemplaza "icon.png" con la ruta de tu imagen de icono
icon_rect = icon.get_rect()

# Definir la posición del icono en la pantalla
icon_position = (100, 100)  # Cambia esto a las coordenadas que desees

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Verificar clic izquierdo
            # Verificar si el clic ocurrió dentro del área del icono
            if icon_rect.collidepoint(event.pos):
                print("colision")
                pygame.quit()
                sys.exit()

    # Dibujar la pantalla
    screen.fill((255, 255, 255))  # Rellenar la pantalla con un color blanco o cualquier otro color que desees

    # Dibujar el icono en la posición deseada
    screen.blit(icon, icon_position)

    # Actualizar la pantalla
    pygame.display.flip()
