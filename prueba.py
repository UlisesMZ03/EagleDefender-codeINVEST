# Import pygame
import pygame

# Initialise pygame
pygame.init()

# Set window size
size = width,height = 600, 600
screen = pygame.display.set_mode(size)

# Clock
clock = pygame.time.Clock()

# Load image
image = pygame.image.load('images/game/texturaConcreto.png').convert_alpha()

# Set the size for the image
DEFAULT_IMAGE_SIZE = (10, 10)

# Rotate the image by any degree
image = pygame.transform.scale(image, DEFAULT_IMAGE_SIZE)

def rotate(angle):
	global image
	rotated_image = pygame.transform.rotate(image, angle)
	rotated_rect = rotated_image.get_rect() # Crea una copia del rectángulo original
	rotated_rect.center =(200,200)   # Mantiene el centro del rectángulo original

	

	
# Set a default position
DEFAULT_IMAGE_POSITION = (200,200)

# Prepare loop condition
running = False

# Event loop
while not running:

	# Close window event
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = True
		elif event.type==pygame.MOUSEBUTTONDOWN:
			if event.button==1:
				image.get_rect().collidepoint(event.pos)
				print("colision")
		elif event.type==pygame.KEYDOWN:
			if event.key==pygame.K_LSHIFT:
				print("shit")
				rotated_image = pygame.transform.rotate(image, 45)
				rotated_rect = rotated_image.get_rect() # Crea una copia del rectángulo original
				rotated_rect.center =(200,200)   # Mantiene el centro del rectángulo original
		x,y=pygame.mouse.get_pos()
		x=x/6
		angulo=180-x
		rotated_image = pygame.transform.rotate(image, angulo)
		rotated_rect = rotated_image.get_rect() # Crea una copia del rectángulo original
		rotated_rect.center =(200,200)   # Mantiene el centro del rectángulo original
					
	
    
	# Background Color
	screen.fill((0, 0, 0))
	print(image.get_rect())

	# Show the image
	screen.blit(rotated_image, rotated_rect)

	# Part of event loop
	pygame.display.flip()
	clock.tick(30)
pygame.quit()
