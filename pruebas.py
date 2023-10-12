import pygame

pygame.init()

# Configuración de la ventana
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Lienzos Pequeños")

# Colores
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Dibuja en el fondo
screen.fill(white)

# Crea dos lienzos pequeños encima del fondo
surface1 = pygame.Surface((300, 100))
surface1.fill(red)
screen.blit(surface1, (100, 200))

surface2 = pygame.Surface((100, 100))
surface2.fill(green)
screen.blit(surface2, (400, 200))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
