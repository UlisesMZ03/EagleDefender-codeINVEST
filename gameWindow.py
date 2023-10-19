import pygame

pygame.init()

# Configuración de la pantalla
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Animación de Sprites")
fondo = pygame.image.load("images/game/floor1.png").convert()
fondo = pygame.transform.scale(fondo, (screen_width, screen_height))
layer = pygame.image.load("images/game/layer1.png").convert_alpha()
layer = pygame.transform.scale(layer, (screen_width, screen_height))
# Cargar el spritesheet con fondo rosa
spritesheet = pygame.image.load("images/game/spritesheet.png")
spritesheet.set_colorkey((255, 0, 255))

# Dimensiones de cada sprite en el spritesheet
sprite_width, sprite_height = 32, 32

# Configuración de las filas del spritesheet para cada dirección de movimiento
DOWN,UP, LEFT, RIGHT, DOWNLEFT, DOWNRIGHT, UPLEFT, UPRIGHT,VICTORY = 0, 1, 2, 3, 4, 5, 6, 7, 8

# Inicializar la dirección de movimiento
current_direction = DOWN

# Posición inicial del sprite
sprite_x, sprite_y = screen_width // 4, screen_height // 2
sprite_speed = 3
sprite_index = 1
# Configurar el reloj para controlar la velocidad de la animación
clock = pygame.time.Clock()


obstaculo_img = pygame.image.load('images/game/Rock1_1_no_shadow.png')
proyectile_img = pygame.image.load('/home/ulisesmz/Escritorio/pro.png')
class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = obstaculo_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        # Lógica de actualización si es necesario
        pass

class Proyectil(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidad):
        super().__init__()
        self.image = proyectile_img
       # Color del proyectil (rojo)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad = velocidad

    def update(self):
        # Mover el proyectil
        self.rect.x += self.velocidad
        # Ocultar el proyectil si sale de la pantalla
        if self.rect.left > screen_width:
            self.kill()  # Eliminar el proyectil del grupo cuando sale de la pantalla

obstaculos = pygame.sprite.Group()
proyectiles = pygame.sprite.Group()

obstaculo = Obstaculo(400, 300)
obstaculos.add(obstaculo)
# Nuevas dimensiones del sprite
nuevo_ancho, nuevo_alto = screen_height/10, screen_height/10
proyectil_velocidad = 5
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                mouse_x, mouse_y = event.pos
                print("hola")
                # Verificar si el nuevo obstáculo colisiona con otros obstáculos existentes
                colision = any(obstaculo.rect.colliderect(pygame.Rect(mouse_x - 32, mouse_y - 32, obstaculo_img.get_width(), obstaculo_img.get_height())) for obstaculo in obstaculos)
                if not colision:
                    nuevo_obstaculo = Obstaculo(mouse_x - 32, mouse_y - 32)
                    obstaculos.add(nuevo_obstaculo)
            else:
                # Disparar un proyectil al hacer clic en la pantalla
                proyectil = Proyectil(*pygame.mouse.get_pos(), proyectil_velocidad)
                proyectiles.add(proyectil)

    
    # Capturar las teclas presionadas
    keys = pygame.key.get_pressed()

    # Cambiar la dirección de movimiento según la tecla presionada
    if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
        current_direction = UPRIGHT
        sprite_y -= sprite_speed
        sprite_x += sprite_speed
        sprite_index = (sprite_index + 1) % 5
    elif keys[pygame.K_UP] and keys[pygame.K_LEFT]:
        current_direction = UPLEFT
        sprite_y -= sprite_speed
        sprite_x -= sprite_speed
        sprite_index = (sprite_index + 1) % 5
    elif keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
        current_direction = DOWNRIGHT
        sprite_y += sprite_speed
        sprite_x += sprite_speed
        sprite_index = (sprite_index + 1) % 5
    elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
        current_direction = DOWNLEFT
        sprite_y += sprite_speed
        sprite_x -= sprite_speed
        sprite_index = (sprite_index + 1) % 5
    elif keys[pygame.K_UP]:
        current_direction = UP
        sprite_y -= sprite_speed
        
        sprite_index = (sprite_index + 1) % 5
    elif keys[pygame.K_DOWN]:
        current_direction = DOWN
        sprite_y += sprite_speed
        sprite_index = (sprite_index + 1) % 5
    elif keys[pygame.K_LEFT]:
        current_direction = LEFT
        sprite_x -= sprite_speed
        sprite_index = (sprite_index + 1) %5
    elif keys[pygame.K_RIGHT]:
        current_direction = RIGHT
        sprite_x += sprite_speed
        sprite_index = (sprite_index + 1) %5


    if sprite_x >= (screen_width/2):
        sprite_x=screen_width//2
    if sprite_x <= (screen_width/7):
        sprite_x=screen_width//7
    if sprite_y <= (screen_height/7):
        sprite_y=screen_height//7
    if sprite_y >= (screen_height/7*6):
        sprite_y=screen_height//7*6
       # Actualizar la pantalla
    screen.blit(fondo, (0, 0))

    # Dibujar los obstáculos
    obstaculos.draw(screen)

    # Actualizar los proyectiles
    proyectiles.update()

    # Detectar colisión entre proyectiles y obstáculos y eliminar los obstáculos
    colisiones = pygame.sprite.groupcollide(obstaculos, proyectiles, True, True)

    # Dibujar los proyectiles
    proyectiles.draw(screen)

    # Obtener el rectángulo del sprite original
    sprite_rect = pygame.Rect(sprite_index * sprite_width, current_direction * sprite_height, sprite_width, sprite_height)
    sprite_original = spritesheet.subsurface(sprite_rect)

    # Escalar el sprite a las nuevas dimensiones
    sprite = pygame.transform.scale(sprite_original, (nuevo_ancho, nuevo_alto))

    # Dibujar el sprite escalado en la pantalla
    screen.blit(sprite, (sprite_x, sprite_y))
    screen.blit(layer, (0, 0))
    pygame.display.flip()
    clock.tick(30)

    # Crear un nuevo obstáculo si todos los obstáculos han sido destruidos
    if not obstaculos:
        nueva_posicion_x = pygame.display.get_surface().get_width() + obstaculo.rect.width
        nueva_posicion_y = pygame.display.get_surface().get_height() // 2
        obstaculo = Obstaculo(nueva_posicion_x, nueva_posicion_y)
        obstaculos.add(obstaculo)

pygame.quit()