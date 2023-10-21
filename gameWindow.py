import pygame
import pyautogui
pygame.init()

# Configuración de la pantalla
transparent_color=(128,128,128,128)# R,G,B, Alpha
size=pyautogui.size()
screen_width, screen_height = size.width,size.height
screen_bloques=pygame.Surface((400,size.height),pygame.SRCALPHA)
screen_bloques.fill(transparent_color)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Animación de Sprites")
fondo = pygame.image.load("images/game/backgrounds/game_background_4.png").convert()
fondo = pygame.transform.scale(fondo, (screen_width, screen_height))
layer = pygame.image.load("images/game/backgrounds/front_layer4.png").convert_alpha()
layer = pygame.transform.scale(layer, (screen_width, screen_height))
# Cargar el spritesheet con fondo rosa


# Configuración de las filas del spritesheet para cada dirección de movimiento
DOWN,UP, LEFT, RIGHT, DOWNLEFT, DOWNRIGHT, UPLEFT, UPRIGHT,VICTORY = 0, 1, 2, 3, 4, 5, 6, 7, 8

# Inicializar la dirección de movimiento
current_direction = DOWN


# Configurar el reloj para controlar la velocidad de la animación
clock = pygame.time.Clock()
nuevo_ancho, nuevo_alto = screen_height/10, screen_height/10
nuevo_ancho_aguila, nuevo_alto_aguila = screen_height/10, screen_height/10*2.66

flag_spsheet2 = pygame.image.load("images/game/Flag/1.1.png")

flagsprite2 = []
for i in range(6):
    sprite = flag_spsheet2.subsurface((i * 32, 0, 32, 64))
    sprite = pygame.transform.scale(sprite, (screen_height/10, screen_height/10*2))
    
    flagsprite2.append(sprite)


flag_spsheet = pygame.image.load("images/game/Flag/1.png")

flagsprite1 = []
for i in range(6):
    sprite = flag_spsheet.subsurface((i * 32, 0, 32, 64))
    sprite = pygame.transform.scale(sprite, (screen_height/10, screen_height/10*2))
    
    flagsprite1.append(sprite)

eagle_spsheet = pygame.image.load("images/game/eagle4.png")

# Definir la lista de imágenes para la animación
frames = []
for i in range(0, 240, 60):
    frame = eagle_spsheet.subsurface(pygame.Rect(i, 0, 60, 160))
    frame = pygame.transform.scale(frame, (screen_height/9, screen_height/9*2.66))
    frames.append(frame)

campfire_spsheet = pygame.image.load("images/game/Campfire/2.png")



# Dividir spritesheet en sprites individuales
campfiresprite = []
for i in range(6):
    sprite = campfire_spsheet.subsurface((i * 32, 0, 32, 32))
    sprite = pygame.transform.scale(sprite, (nuevo_ancho, nuevo_ancho*1.64))
    
    campfiresprite.append(sprite)


current_frame = 0
animation_speed = 10  # Velocidad de la animación (cambia este valor para ajustar la velocidad)
frame_counter = 0


obstaculo_img = pygame.image.load('images/game/Rock1_1_no_shadow.png')
proyectile_img = pygame.image.load('images/game/Rock1_1_no_shadow.png')
class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, x,y,img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.active_box=None
        self.angle = 0 

    def update(self):
        # Lógica de actualización si es necesario

        pass
    def draw(self,surface):
        print('dibujando')
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rect = rotated_image.get_rect(center=self.rect.center)
        surface.blit(rotated_image, rect.topleft)


        
        
    def rotate(self,angle_change):
        self.angle += angle_change
        if self.angle >= 360:
            self.angle -= 360
        if self.angle < 0:
            self.angle += 360
    def dragg(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print('presiono el boton')
                if self.rect.collidepoint(event.pos):
                    print("objeto")
                    self.active_box = self.rect

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                   self.active_box = None

        if event.type == pygame.MOUSEMOTION:
            if self.active_box is not None:
                self.active_box.move_ip(event.rel)
    
    def handle_key_event(self, key_event):
        if key_event.type == pygame.KEYDOWN:
            if key_event.unicode == 'r':
                self.rotate(-90)  # Rotate 90 degrees counterclockwise on 'r' key press
            elif key_event.unicode == 't':
                self.rotate(90)  # Rotate 90 degrees clockwise on 't' key press



class Defensor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprite_width, self.sprite_height = 60, 160
        self.spritesheet = pygame.image.load("images/game/eagle4.png")
        self.spritesheet.set_colorkey((255, 0, 255))
        self.current_frame = 0
        
        self.animation_speed = 1  # Velocidad de la animación (ajusta según sea necesario)
        self.image = self.get_current_sprite()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def get_current_sprite(self):
        sprite_rect = pygame.Rect(
            self.current_frame%4 * self.sprite_width,
            0,  # Ya que todas las imágenes están en la misma fila
            self.sprite_width,
            self.sprite_height
        )
        sprite_original = self.spritesheet.subsurface(sprite_rect)
        return pygame.transform.scale(sprite_original, (int(nuevo_ancho_aguila), int(nuevo_alto_aguila)))

    def update(self):
        self.animation_speed+=1
        if self.animation_speed==10:

            self.current_frame += 1
            self.image = self.get_current_sprite()
            self.animation_speed=0

class Atacante(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprite_width = 32
        self.sprite_height = 32
        self.sprite_speed = 3
        self.sprite_index = 1
        self.spritesheet = pygame.image.load("images/game/spritesheet.png")
        self.spritesheet.set_colorkey((255, 0, 255))
        self.current_direction = DOWN  # Puedes establecer la dirección inicial
        self.image = self.get_current_sprite()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def get_current_sprite(self):
        sprite_rect = pygame.Rect(
            self.sprite_index%5 * self.sprite_width,
            self.current_direction * self.sprite_height,
            self.sprite_width,
            self.sprite_height
        )
        sprite_original = self.spritesheet.subsurface(sprite_rect)
        return pygame.transform.scale(sprite_original, (nuevo_ancho, nuevo_alto))

    def update(self):
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            self.rect.y -= self.sprite_speed
            self.rect.x += self.sprite_speed
            self.current_direction = UPRIGHT
            self.sprite_index+=1
        elif keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            self.rect.y -= self.sprite_speed
            self.rect.x -= self.sprite_speed
            self.current_direction = UPLEFT
            self.sprite_index+=1
        elif keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
            self.rect.y += self.sprite_speed
            self.rect.x += self.sprite_speed
            self.current_direction = DOWNRIGHT
            self.sprite_index+=1
        elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
            self.rect.y += self.sprite_speed
            self.rect.x -= self.sprite_speed
            self.current_direction = DOWNLEFT
            self.sprite_index+=1
        elif keys[pygame.K_UP]:
            self.rect.y -= self.sprite_speed
            self.current_direction = UP
            self.sprite_index+=1
        elif keys[pygame.K_DOWN]:
            self.rect.y += self.sprite_speed
            self.current_direction = DOWN
            self.sprite_index+=1
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.sprite_speed
            self.current_direction = LEFT
            self.sprite_index+=1
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.sprite_speed
            self.current_direction = RIGHT
            self.sprite_index+=1



        # Limitar la posición del sprite dentro de la pantalla si es necesario
        self.rect.x = max(screen_width // 2, min(screen_width // 8 * 7, self.rect.x))
        self.rect.y = max(screen_height // 8 * 2 + nuevo_alto // 4, min(screen_height // 8 * 7, self.rect.y))

        # Actualizar el sprite actual
        self.image = self.get_current_sprite()

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
        self.rect.x -= self.velocidad
        # Ocultar el proyectil si sale de la pantalla
        if self.rect.left > screen_width:
            self.kill()  # Eliminar el proyectil del grupo cuando sale de la pantalla

obstaculos = pygame.sprite.Group()
proyectiles = pygame.sprite.Group()

obstaculo = Obstaculo(size.width-370, size.height//2, obstaculo_img)
obstaculos.add(obstaculo)


# Nuevas dimensiones del sprite
atacante = Atacante(screen_width // 2, screen_height // 2)
defensor = Defensor(screen_width // 8 - 42, screen_height // 2 - 37)
proyectil_velocidad = 5
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
       

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                mouse_x, mouse_y = event.pos
                if mouse_x<screen_width//2 and mouse_x>screen_width//8 and mouse_y>=screen_height//8*2+ screen_height//10 and mouse_y<screen_height//8*7+screen_height//10:

                    # Verificar si el nuevo obstáculo colisiona con otros obstáculos existentes
                    colision = any(obstaculo.rect.colliderect(pygame.Rect(mouse_x - 32, mouse_y - 32, obstaculo_img.get_width(), obstaculo_img.get_height())) for obstaculo in obstaculos)
                    if not colision:
                        nuevo_obstaculo = Obstaculo(mouse_x - 32, mouse_y - 32)
                        obstaculos.add(nuevo_obstaculo)
            else:
                # Disparar un proyectil al hacer clic en la pantalla
                proyectil = Proyectil(atacante.rect.x+nuevo_ancho/2,atacante.rect.y+nuevo_alto/2, proyectil_velocidad)
                proyectiles.add(proyectil)
        obstaculo.dragg(event)
        obstaculo.handle_key_event(event)
       

  

    # Detectar colisión entre proyectiles y obstáculos y eliminar los obstáculos
    colisiones = pygame.sprite.groupcollide(obstaculos, proyectiles, True, True)
    # Actualizar el atacante
    

    # Dibujar el atacante en la pantalla
    screen.blit(fondo, (0, 0))
    obstaculos.update()
    obstaculos.draw(screen)
    atacante.update()
    # Actualizar el águila
    defensor.update()
    screen.blit(defensor.image, defensor.rect)
    screen.blit(atacante.image, atacante.rect)
    # Dibujar los proyectiles
    proyectiles.update()
    proyectiles.draw(screen)
    obstaculo.draw(screen)


    
    frame_counter += 1
    if frame_counter >= animation_speed:
        frame_counter = 0  # Reiniciar el contador
        current_frame = (current_frame + 1) % 100

    screen.blit(flagsprite2[current_frame%len(flagsprite2)], (screen_width // 8 - 32, screen_height //8*2 - screen_height//10))

    screen.blit(flagsprite2[current_frame%len(flagsprite2)], (screen_width // 8 - 32, screen_height //8*7 - screen_height//10))
    screen.blit(flagsprite1[current_frame%len(flagsprite1)], (screen_width // 8*7 - 32, screen_height //8*2 - screen_height//10))
    
    screen.blit(flagsprite1[current_frame%len(flagsprite1)], (screen_width // 8*7 - 32, screen_height //8*7 - screen_height//10))
    

    screen.blit(campfiresprite[current_frame%len(campfiresprite)], (screen_width // 22*21 - 32, screen_height // 8*3))
    screen.blit(layer, (0, 45))
    screen.blit(screen_bloques,(size.width-400,0))

    pygame.display.flip()
    clock.tick(75)
    # Crear un nuevo obstáculo si todos los obstáculos han sido destruidos
    if not obstaculos:
        nueva_posicion_x = pygame.display.get_surface().get_width() + obstaculo.rect.width
        nueva_posicion_y = pygame.display.get_surface().get_height() // 2
        obstaculo = Obstaculo(nueva_posicion_x, nueva_posicion_y,obstaculo_img)
        obstaculos.add(obstaculo)

pygame.quit()