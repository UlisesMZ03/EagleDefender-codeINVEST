import pygame
import pyautogui
import sys
pygame.init()

# Configuración de la pantalla
transparent_color=(128,128,128,128)# R,G,B, Alpha
size=pyautogui.size()
screen_width, screen_height = size.width,size.height

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


nuevo_tamano=(100,100/2+20)
tamano_textrura=(30,10)
tam_primerElemento=(50,50//3)
#cargando imagenes
textura_madera=pygame.image.load('images/game/texturaMadera.png')
textura_madera=pygame.transform.smoothscale(textura_madera,tamano_textrura)
textura_maderaElem1=pygame.transform.smoothscale(textura_madera,tam_primerElemento)

textura_piedra=pygame.image.load('images/game/texturaPiedra.jpeg')
textura_piedra=pygame.transform.smoothscale(textura_piedra,tamano_textrura)
textura_piedraElem1=pygame.transform.smoothscale(textura_piedra,tam_primerElemento)


textura_concreto=pygame.image.load('images/game/texturaConcreto.png')
textura_concreto=pygame.transform.smoothscale(textura_concreto,tamano_textrura)
textura_concretoElem1=pygame.transform.smoothscale(textura_concreto,tam_primerElemento)

obstaculoMadera = pygame.image.load('images/game/madera4.png').convert_alpha()
obstaculoPiedra=pygame.image.load('images/game/bloquePiedra.png').convert_alpha()
obstaculoPiedra=pygame.transform.smoothscale(obstaculoPiedra,nuevo_tamano).convert_alpha()
obstaculoMadera = pygame.transform.smoothscale(obstaculoMadera, nuevo_tamano).convert_alpha()

obstaculoConcreto= pygame.image.load('images/game/bloqueConcreto.png').convert_alpha()
obstaculoConcreto = pygame.transform.smoothscale(obstaculoConcreto, nuevo_tamano).convert_alpha()

proyectile_img = pygame.image.load('images/game/Rock1_1_no_shadow.png')

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, x,y,img,obst_img):
        super().__init__()
        self.imgBefore=img
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = 0
        self.obs_img=obst_img
        self.offset=(0,0)
        self.dragging=False
        self.is_rotate=False
        self.dragging_offset = (0, 0)
        self.originalPosition=(x,y)

    def imgBack(self):
        self.image = self.imgBefore

    def rotate(self,angle_change):
        self.angle += angle_change
        if self.angle >= 360:
            self.angle -= 360
        if self.angle < 0:
            self.angle += 360
         # Rotar la imagen original

        self.image = pygame.transform.rotate(self.image, self.angle)
        # Actualizar el rectángulo con la nueva imagen
        self.rect = self.image.get_rect(center=self.rect.center)  


    def start_dragg(self):
        self.dragging=True
     
    
    def stop_dragg(self):
        self.dragging=False
        
    def drag(self,pos):
        if self.dragging:
            self.rect.center=pos
            
    def changeImg(self,pos):
        if not self.dragging:
            obstaculos.remove(self)
            self.image=self.obs_img
            self.rect = self.image.get_rect()
            self.rect.center=pos
          
            obstaculos.add(self) 
           

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
        if self.rect.left < 400:
            self.kill()  # Eliminar el proyectil del grupo cuando sale de la pantalla

obstaculos = pygame.sprite.Group()

proyectiles = pygame.sprite.Group()



# Nuevas dimensiones del sprite
atacante = Atacante(screen_width // 2, screen_height // 2)
defensor = Defensor(screen_width // 8 - 42, screen_height // 2 - 37)
proyectil_velocidad = 5
running = True
obstaculodrag=None

def agregarBloquesEstante(cant,x,y,texturaElem1,textura,bloque_img):
    for i in range(cant):
        if i==0:
            obstaculos.add(Obstaculo(x-i*35,y-((50//3)//2)+5,texturaElem1,bloque_img))
        else:
            obstaculos.add(Obstaculo(x-i*35,y,textura,bloque_img))


def check_collision(block, group):
    for other_block in group:
        if block != other_block and block.rect.colliderect(other_block.rect):
            return True
    return False
obstaculodrag=None
offset_x, offset_y = 0, 0
dragging=False

agregarBloquesEstante(10,330,size.height//2-100,textura_maderaElem1,textura_madera,obstaculoMadera)
agregarBloquesEstante(10,330,size.height//2-50,textura_piedraElem1,textura_piedra,obstaculoPiedra)
agregarBloquesEstante(10,330,size.height//2-150,textura_concretoElem1,textura_concreto,obstaculoConcreto)

while running:
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for obstaculo in obstaculos:
                    if obstaculo.rect.collidepoint(event.pos):
                        obstaculo.start_dragg()
                        obstaculodrag = obstaculo
                        dragging=True
                        break
                        
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                
                if obstaculodrag:
                    dragging=False
                    obstaculodrag.stop_dragg()
                    obstaculodrag.changeImg(event.pos)
                    mouse_x, mouse_y = event.pos
                    #Verificar que no se coloque el bloque en el area enemiga
                    if mouse_x<screen_width//2 and mouse_x>screen_width//8 and mouse_y>=screen_height//8*2+ screen_height//10 and mouse_y<screen_height//8*7+screen_height//10:
 
                        if check_collision(obstaculodrag, obstaculos):
                            obstaculodrag.rect.center=obstaculodrag.originalPosition
                                #obstaculodrag.imgBack()
                            print('colision')
                        obstaculodrag = None
                    # Clear the dragging flag
            if event.button==3:
                proyectil = Proyectil(atacante.rect.x+nuevo_ancho/2,atacante.rect.y+nuevo_alto/2, proyectil_velocidad)
                proyectiles.add(proyectil)

        if event.type == pygame.MOUSEMOTION:
            if obstaculodrag:  # Check the dragging flag
               obstaculodrag.rect.move_ip(event.rel)

        elif event.type == pygame.KEYDOWN:
            print(f'presionando tecla´{event.key}')
            if event.key == pygame.K_LSHIFT:  # Verifica si se presionó la tecla Shift derecha
                if obstaculodrag:
                    obstaculodrag.rotate(90) 
            

    # Detectar colisión entre proyectiles y obstáculos y eliminar los obstáculos
    colisiones = pygame.sprite.groupcollide(obstaculos, proyectiles, True, True)
    # Actualizar el atacante
    
   
    # Dibujar el atacante en la pantalla
    screen.blit(fondo, (0, 0))
   
    obstaculos.draw(screen)
    atacante.update()
    # Actualizar el águila
    defensor.update()
    screen.blit(defensor.image, defensor.rect)
    screen.blit(atacante.image, atacante.rect)
    # Dibujar los proyectiles
    proyectiles.update()
    proyectiles.draw(screen)
    #actualiza los obstaculos
 


    
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
   

    




    pygame.display.flip()
    clock.tick(75)
    # Crear un nuevo obstáculo si todos los obstáculos han sido destruidos
    

pygame.quit()