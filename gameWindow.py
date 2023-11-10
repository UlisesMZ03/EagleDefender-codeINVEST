import pygame
import math
from objectbasedata import Musica
from objectbasedata  import Usuario
from objectbasedata  import Score
import webbrowser as web
import pyautogui
from time import sleep
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import webbrowser
import os



def game(lista):
    pygame.init()
    pygame.mixer.init()
    # Obtener información sobre la pantalla del sistema
    BACKGROUND = '#005b4d'
    PCBUTTON = '#01F0BF'
    SCBUTTON = '#00A383'
    TCBUTTOM = '#006350'
    screen_info = pygame.display.Info()
    

    font = pygame.font.Font("font/KarmaFuture.ttf", 36)
    # Configuración de la pantalla
    screen_width, screen_height = screen_info.current_w, screen_info.current_h

    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

    pygame.display.set_caption("Animación de Sprites")
    fondo = pygame.image.load("images/game/backgrounds/game_background_4.png").convert()
    fondo = pygame.transform.scale(fondo, (screen_width, screen_height))
    layer = pygame.image.load("images/game/backgrounds/front_layer4.png").convert_alpha()
    layer = pygame.transform.scale(layer, (screen_width, screen_height))
    # Cargar el spritesheet con fondo rosa
    # Cargar la imagen powers.png
    WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
    powers_image = pygame.image.load("images/game/powers/power_inventory.png")
    powers_image = pygame.transform.scale(powers_image, (screen_width/8.5, screen_height/3.5))
    camera_preview_rect = pygame.Rect(WIDTH/7*4, HEIGHT/14.4*3, WIDTH/7*2-55, HEIGHT/14.4*4)

    #camera_image = None  # Inicializar la imagen de la cámara fuera del bucle princUIDal
    #initial_image_surface = pygame.transform.scale(image_pp, (camera_preview_rect.width, camera_preview_rect.height))


    profile_surface = pygame.Surface((camera_preview_rect.width, camera_preview_rect.height))
    profile_surface.fill(SCBUTTON)

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
    nuevo_tamano=(150//3,150)
    tamano_textrura=(20,20)
    tam_primerElemento=(40,40)
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

    obstaculo_img = pygame.image.load('images/game/Rock1_1_no_shadow.png')
    proyectile_img = pygame.image.load('images/game/Rock1_1_no_shadow.png')
    # Inicializa el cliente de Spotipy
    SPOTIPY_CLIENT_SECRET="0db3c2314d794ef28b594b4d24b07fe9"
    SPOTIPY_CLIENT_ID="8051e3ec08d240639f7cad6370e88a67"
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))

    """
    def get_spotify_track_url(track_id):
        track_info = sp.track(track_id)
        track_url = track_info['external_urls']['spotify']
        return track_url

    def music(username):
        userName_encript = Usuario.encripta(username)
        username1 = Usuario.getID(userName_encript)
        
        musica_user = Musica.getMusic(username1)
        print(musica_user)
        size = len(musica_user)
        n = random.randint(0, size - 1)
        track_id = musica_user[n][0]  # Asegúrate de obtener el ID de la pista de la lista de música
        track_url = get_spotify_track_url(track_id)
        webbrowser.open(track_url)"""
    def music(username):
        id=Usuario.getID(username)
        musica_user = Musica.getMusic(id)
        size = len(musica_user)
        n = random.randint(0, size - 1)
        
    def load_selected_image(image_path):
        if os.path.exists(image_path):
            image_surface = pygame.image.load(image_path).convert()
            return pygame.transform.scale(image_surface, (150,150))
        return None
    

    
    def calcular_puntaje(bloques_destruidos, tiempo_ataque):
        if tiempo_ataque == 0 or bloques_destruidos==0:
            return 0  # división por cero
        media_armonica = 2 / ((0.5 / bloques_destruidos) + (0.5 / tiempo_ataque))
        return media_armonica





    class Obstaculo(pygame.sprite.Sprite):
        def __init__(self, x,y,img,obst_img, tipo):
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
            self.filter=False
            self.is_active = False
            self.tipo=tipo
            self.sound=pygame.mixer.Sound('sounds/explosion.mp3')
            
        def activate(self):
            # Logic to activate/placement of the object
            # You can customize this logic based on your requirements
            self.is_active = True

        def deactivate(self):
            print("desactivado")
            # Logic to deactivate/unplace the object
            self.is_active = False
        def addFilter(self,image):
            if self.filter:
                self.red_filtered = image.copy()
                self.red_filtered.fill((255, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                self.image=self.red_filtered

        def filter_active(self):
            self.filter=True

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
            
            self.vida = 3  # Inicializa la vida del defensor

        def get_current_sprite(self):
            sprite_rect = pygame.Rect(
                self.current_frame % 4 * self.sprite_width,
                0,  # Ya que todas las imágenes están en la misma fila
                self.sprite_width,
                self.sprite_height
            )
            sprite_original = self.spritesheet.subsurface(sprite_rect)
            return pygame.transform.scale(sprite_original, (int(nuevo_ancho_aguila), int(nuevo_alto_aguila)))

        def recibir_dano(self, dano):
            print(self.vida)
            self.vida -= dano


        def update(self):
            self.animation_speed += 1
            if self.animation_speed == 10:
                self.current_frame += 1
                self.image = self.get_current_sprite()
                self.animation_speed = 0

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
            self.bolas_fuego = 5  # Número inicial de bolas de fuego disponibles
            self.bolas_agua = 3  # Número inicial de bolas de agua disponibles
            self.bolas_polvora = 10  # Número inicial de bolas de pólvora disponibles

        def lanzar_bola_fuego(self):
            if self.bolas_fuego > 0:
                # Lógica para lanzar una bola de fuego
                self.bolas_fuego -= 1

        def lanzar_bola_agua(self):
            if self.bolas_agua > 0:
                # Lógica para lanzar una bola de agua
                self.bolas_agua -= 1

        def lanzar_bola_polvora(self):
            if self.bolas_polvora > 0:
                # Lógica para lanzar una bola de pólvora
                self.bolas_polvora -= 1

        def recoger_bolas(self, bolas_fuego=0, bolas_agua=0, bolas_polvora=0):
            # Método para que el personaje recoja más bolas durante el juego
            self.bolas_fuego += bolas_fuego
            self.bolas_agua += bolas_agua
            self.bolas_polvora += bolas_polvora

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

            if keys[pygame.K_w] and keys[pygame.K_d] and not eagle_defeat:
                self.rect.y -= self.sprite_speed
                self.rect.x += self.sprite_speed
                self.current_direction = UPRIGHT
                self.sprite_index+=1
            elif keys[pygame.K_w] and keys[pygame.K_a] and not eagle_defeat:
                self.rect.y -= self.sprite_speed
                self.rect.x -= self.sprite_speed
                self.current_direction = UPLEFT
                self.sprite_index+=1
            elif keys[pygame.K_s] and keys[pygame.K_d] and not eagle_defeat:
                self.rect.y += self.sprite_speed
                self.rect.x += self.sprite_speed
                self.current_direction = DOWNRIGHT
                self.sprite_index+=1
            elif keys[pygame.K_s] and keys[pygame.K_a] and not eagle_defeat:
                self.rect.y += self.sprite_speed
                self.rect.x -= self.sprite_speed
                self.current_direction = DOWNLEFT
                self.sprite_index+=1
            elif keys[pygame.K_w] and not eagle_defeat:
                self.rect.y -= self.sprite_speed
                self.current_direction = UP
                self.sprite_index+=1
            elif keys[pygame.K_s] and not eagle_defeat:
                self.rect.y += self.sprite_speed
                self.current_direction = DOWN
                self.sprite_index+=1
            elif keys[pygame.K_a] and not eagle_defeat:
                self.rect.x -= self.sprite_speed
                self.current_direction = LEFT
                self.sprite_index+=1
            elif keys[pygame.K_d] and not eagle_defeat:
                self.rect.x += self.sprite_speed
                self.current_direction = RIGHT
                self.sprite_index+=1



            # Limitar la posición del sprite dentro de la pantalla si es necesario
            self.rect.x = max(screen_width // 2, min(screen_width // 8 * 7, self.rect.x))
            self.rect.y = max(screen_height // 8 * 2 + nuevo_alto // 4, min(screen_height // 8 * 7, self.rect.y))

            # Actualizar el sprite actual
            self.image = self.get_current_sprite()

        
    class Proyectil(pygame.sprite.Sprite):
        def __init__(self, x, y, velocidad, angulo, tipo):
            super().__init__()
            self.tipo = tipo  # Almacena el tipo de proyectil (agua, fuego, polvora)
            if self.tipo == "agua":
                self.spritesheet = pygame.image.load("images/game/powers/water.png")
                self.sound = pygame.mixer.Sound('sounds/water.mp3')
            elif self.tipo == "fuego":
                self.spritesheet = pygame.image.load("images/game/powers/fire.png")
                self.sound = pygame.mixer.Sound('sounds/fireball.mp3')
            elif self.tipo == "polvora":
                self.spritesheet = pygame.image.load("images/game/powers/powder.png")
                self.sound = pygame.mixer.Sound('sounds/firework.mp3')


            self.current_frame = 0  # Inicializar el índice del fotograma actual
            self.frames = []  # Lista para almacenar las imágenes individuales del spritesheet
            self.load_frames()  # Cargar las imágenes del spritesheet en la lista de frames
            self.angulo=angulo
            # Establecer la imagen inicial del proyectil
            self.image = self.frames[self.current_frame]
           
            
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.velocidad = velocidad

            # Calcular componentes de dirección basadas en el ángulo
            self.direction_x = math.cos(math.radians(angulo))
            self.direction_y = -math.sin(math.radians(angulo))

            #pygame.mixer.music.load('sounds/login.mp3')

        def load_frames(self):
            # Dividir el spritesheet en imágenes individuales y añadirlas a la lista de frames
            # Asumiendo que el spritesheet contiene 5 imágenes en una fila
            frame_width = self.spritesheet.get_width() // 5
            frame_height = self.spritesheet.get_height()
            for i in range(5):
                frame = self.spritesheet.subsurface((i * frame_width, 0, frame_width, frame_height))
                self.frames.append(frame)
        contador=0

        def update(self):
            self.contador+=1
            # Cambiar la imagen del proyectil en cada fotograma para crear la animación
            if self.contador==8:
                self.contador=0
                self.current_frame = (self.current_frame + 1) % 5  # Cambiar al siguiente fotograma
            self.image = self.frames[self.current_frame]  # Establecer la nueva imagen del proyectil
            # Rotar la imagen del proyectil según el ángulo (en grados)
            self.image = pygame.transform.rotate(self.image, self.angulo)
            
            # Mover el proyectil en la dirección calculada
            self.rect.x += self.velocidad * self.direction_x
            self.rect.y += self.velocidad * self.direction_y

            # Verificar si el proyectil ha salido de los límites de la pantalla y eliminarlo
            if self.rect.left > screen_width or self.rect.right < 0 or self.rect.top > screen_height or self.rect.bottom < 0:
                self.kill()





    class Mirilla(pygame.sprite.Sprite):

        def __init__(self, sprite, offset=(0, 0), angular_speed=0.1):
            super().__init__()
            self.sprite = sprite
            self.offset = offset
            self.angular_speed = angular_speed
            self.angle = 0
            self.last_update = pygame.time.get_ticks()
            self.radius = 40
            self.image_original = pygame.image.load("images/game/flecha.png")
            self.image_original = pygame.transform.scale(self.image_original, (40, 40))
            self.image = self.image_original.copy()
            self.rect = self.image.get_rect()
            self.update_position()

        def get_tip_position(self):
            angle_rad = math.radians(self.angle)
            tip_x = self.sprite.rect.centerx + self.radius * math.cos(angle_rad)
            tip_y = self.sprite.rect.centery + self.radius * math.sin(angle_rad)
            return tip_x, tip_y

        def update_position(self):
            center_x, center_y = self.sprite.rect.center
            self.rect.centerx = center_x + self.radius * math.cos(math.radians(self.angle))
            self.rect.centery = center_y + self.radius * math.sin(math.radians(self.angle))
        def update(self):
                self.update_position()
                now = pygame.time.get_ticks()
                elapsed_time = now - self.last_update
                self.last_update = now
                self.angle += self.angular_speed * elapsed_time
                self.angle %= 360
                self.image = pygame.transform.rotate(self.image_original, -self.angle)
                self.rect = self.image.get_rect(center=self.rect.center)
    
    def agregarBloquesEstante(cant,x,y,texturaElem1,textura,bloque_img,tipo):

        for i in range(cant):
            obstaculos.add(Obstaculo(x-i*25,y,textura,bloque_img,tipo))
    
    
        m_x=0
        c_x=0
        p_x=0
        for obstaculo in obstaculos:
            
            if not obstaculo.is_active:
                if obstaculo.tipo=="madera" and m_x<10:
                    m_x+=1
                    obstaculo.rect.y = obstaculo.originalPosition[1]
                    obstaculo.rect.x = 22*m_x
                elif obstaculo.tipo=="piedra"and c_x<10:
                    p_x+=1
                    obstaculo.rect.y = obstaculo.originalPosition[1]
                    obstaculo.rect.x = 22*p_x
                elif obstaculo.tipo=="concreto"and c_x<10:
                    c_x+=1
                    obstaculo.rect.y = obstaculo.originalPosition[1]
                    obstaculo.rect.x = 22*c_x
    

    def check_collision(block, group):
        for other_block in group:
            if block != other_block and block.rect.colliderect(other_block.rect):
                return True
        return False
    esperando_tecla = True
    TITLE_FONT = pygame.font.Font("font/KarmaFuture.ttf", 50)
    FONT = pygame.font.Font("font/DejaVuSans.ttf", 20)
    FONT_SEC = pygame.font.Font("font/DejaVuSans.ttf", 20)
    running = True
    ronda = 1
    puntajes_user1= []
    puntajes_user2= []
    while running:
        

        obstaculos = pygame.sprite.Group()
        # Definir el color del círculo (en RGB)
        circle_color = (255, 0, 0)

        # Suponiendo que tienes una variable llamada cantidad_circulos
        cantidad_circulos = 7 


        # Nuevas dimensiones del sprite
        atacante = Atacante(screen_width // 2, screen_height // 2)
        
        proyectiles = pygame.sprite.Group()
        todos_los_sprites = pygame.sprite.Group()  
        obstaculos_activos = pygame.sprite.Group()
        obstaculos_inactivos = pygame.sprite.Group()
        mirilla = Mirilla(atacante, offset=(0, 0))
        todos_los_sprites.add(mirilla)  
        proyectil_velocidad = 5
        
        
        obstaculodrag=None
        offset_x, offset_y = 0, 0
        dragging=False
        ROJO_TRANSPARENTE = (255, 0, 0, 128)
        agregarBloquesEstante(10,150,screen_height//2-100,textura_maderaElem1,textura_madera,obstaculoMadera,"madera")
        agregarBloquesEstante(10,150,screen_height//2-50,textura_piedraElem1,textura_piedra,obstaculoPiedra,"piedra")
        agregarBloquesEstante(10,150,screen_height//2-150,textura_concretoElem1,textura_concreto,obstaculoConcreto,"concreto")

        eagle_defeat = False
        defensor_done=False
        obs_done=False
        tiempo_ataque_atacante = 300
        tiempo_defensa_defensor = 300

        
        obstaculos_destruidos = 0

        # Definir la variable para almacenar el tiempo en segundos
        tiempo_segundos = 0
        selected_image_surface1 = load_selected_image(f'./profile_photos/{Usuario.getID(lista[0])}.png')  # Establecer la imagen inicial
        selected_image_surface2 = load_selected_image(f'./profile_photos/{Usuario.getID(lista[1])}.png')  # Establecer la imagen inicial
        #profile_surface.blit(selected_image_surface, (0, 0))
        score_saved=False
        while ronda<=3:
            print("obstaculos"+str(len(obstaculos)))
            round_surface = TITLE_FONT.render("Login", True, PCBUTTON)  # Color blanco (#FFFFFF)
            round_rect = round_surface.get_rect(center=(WIDTH // 2, 50))  # Ajusta las coordenadas según la posición que desees

            print(ronda)
            screen.blit(fondo, (0, 0))
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ronda=5
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN and not eagle_defeat and defensor_done:
                    if event.button == 1:
                        for obstaculo in obstaculos:
                            if obstaculo.rect.collidepoint(event.pos):
                                obstaculo.start_dragg()
                                
                                obstaculodrag = obstaculo
                                
                                dragging=True
                                break
                                
                if event.type == pygame.MOUSEBUTTONDOWN and not eagle_defeat and not defensor_done:
                    if event.button == 1:
                        mouse_x, mouse_y = event.pos
                        if mouse_x<screen_width//2 and mouse_x>screen_width//8 and mouse_y>=screen_height//8*2+ screen_height//10 and mouse_y<screen_height//8*7+screen_height//10:
                            defensor = Defensor(mouse_x- 42, mouse_y- 37)
                            defensor_done=True
                        
                if event.type == pygame.MOUSEBUTTONUP and not eagle_defeat:
                    if event.button == 1:
                        
                        if obstaculodrag:
                            dragging=False
                            if not obstaculodrag.is_active:
                                obstaculodrag.activate()
                                obstaculodrag.stop_dragg()
                                obstaculodrag.changeImg(event.pos)
                            mouse_x, mouse_y = event.pos
                            #Verificar que no se coloque el bloque en el area enemiga
                            if mouse_x<screen_width//2 and mouse_x>screen_width//8 and mouse_y>=screen_height//8*2+ screen_height//10 and mouse_y<screen_height//8*7+screen_height//10:
                                #obstaculodrag.image=obstaculodrag.obs_img
                                if check_collision(obstaculodrag, obstaculos):
                                    obstaculodrag.imgBack()
                                    obstaculodrag.deactivate()
                                    obstaculodrag.changeImg(event.pos)
                                    obstaculodrag.rect.x=obstaculodrag.originalPosition[0]
                                    
                                    
                                    
                                
                                    print('colision')
                                obstaculodrag = None
                            else:
                                #obstaculodrag.image.fill(ROJO_TRANSPARENTE)
                                obstaculodrag.filter_active()
                                obstaculodrag.addFilter(obstaculodrag.image)
                            # Clear the dragging flag


                if event.type == pygame.MOUSEMOTION and not eagle_defeat:
                    if obstaculodrag:  # Check the dragging flag
                            
                        obstaculodrag.rect.move_ip(event.rel)

                elif event.type == pygame.KEYDOWN and not eagle_defeat:
        
                    if event.key == pygame.K_LSHIFT:  # Verifica si se presionó la tecla Shift derecha
                        if obstaculodrag:
                            obstaculodrag.rotate(45) 

                    if event.key == pygame.K_j and not eagle_defeat and defensor_done and obs_done:  # Se presiona la letra 'j'
                        if atacante.bolas_fuego>0:
                            tip_x, tip_y = mirilla.get_tip_position()
                            angle_rad = mirilla.angle
                            proyectil = Proyectil(tip_x, tip_y, proyectil_velocidad, -angle_rad, "fuego")
                            proyectil.sound.play()
                            proyectiles.add(proyectil)
                            atacante.lanzar_bola_fuego()
                    if event.key == pygame.K_k and not eagle_defeat and defensor_done and obs_done:  # Se presiona la letra 'j'
                        if atacante.bolas_agua>0:
                            tip_x, tip_y = mirilla.get_tip_position()
                            angle_rad = mirilla.angle
                            proyectil = Proyectil(tip_x, tip_y, proyectil_velocidad, -angle_rad, "agua")
                            proyectil.sound.play()
                            proyectiles.add(proyectil)
                            atacante.lanzar_bola_agua()
                    if event.key == pygame.K_l and not eagle_defeat and defensor_done and obs_done:  # Se presiona la letra 'j'
                        if atacante.bolas_polvora>0:
                            tip_x, tip_y = mirilla.get_tip_position()
                            angle_rad = mirilla.angle
                            proyectil = Proyectil(tip_x, tip_y, proyectil_velocidad, -angle_rad, "polvora")
                            proyectil.sound.play()
                            proyectiles.add(proyectil)
                            atacante.lanzar_bola_polvora()
            
            obstaculos_activos.empty()
            for obstaculo in obstaculos:
                if obstaculo.is_active:
                    obstaculos_activos.add(obstaculo)
            obstaculos_inactivos.empty()
            for obstaculo in obstaculos:
                if not obstaculo.is_active:
                    obstaculos_inactivos.add(obstaculo)
            
            if len(obstaculos_activos)>=5:
                    obs_done=True
            
            agregarBloquesEstante(0,150,screen_height//2-100,textura_maderaElem1,textura_madera,obstaculoMadera,"madera")
            colisiones = pygame.sprite.groupcollide(obstaculos_activos, proyectiles, True, True)
            if defensor_done:
                colisiones_defensor = pygame.sprite.spritecollide(defensor, proyectiles, True)
                if colisiones_defensor:
                    if proyectil.tipo=="agua":

                        defensor.recibir_dano(1)
                    elif proyectil.tipo=="fuego":
                        defensor.recibir_dano(2)
                    elif proyectil.tipo=="polvora":
                        defensor.recibir_dano(4)

                    if defensor.vida<=0:
                        eagle_defeat=True

            if colisiones:
                pygame.mixer.Sound('sounds/explosion.mp3').play()
                obstaculos_destruidos += len(colisiones)
                print(obstaculos_destruidos)
                # Verificar la vida del defensor

        # agregarBloquesEstante(0,150,screen_height//2-100,textura_maderaElem1,textura_madera,obstaculoMadera,"madera")
            # Dibujar el atacante en la pantalla
            screen.blit(flagsprite1[current_frame%len(flagsprite1)], (screen_width // 8*7 - 32, screen_height //8*2 - screen_height//10))
            
            screen.blit(atacante.image, atacante.rect)
            atacante.update()
            # Actualizar el águila
            if eagle_defeat:
                texto = font.render("El atacante ha ganado", True, (255, 255, 255))
                puntos_atacante= tiempo_segundos
                if ronda==1:
                    texto = font.render("El defensor "+str(lista[1])+" ha ganado", True, (255, 255, 255))
                    puntajes_user2.append(puntos_atacante)
                elif ronda==2:
                    texto = font.render("El defensor "+str(lista[0])+" ha ganado", True, (255, 255, 255))
                    puntajes_user1.append(puntos_atacante)
                elif ronda==3:
                    texto = font.render("El defensor "+str(lista[1])+" ha ganado", True, (255, 255, 255))
                    puntajes_user2.append(puntos_atacante)

                if len(puntajes_user1)>1:
                    puntuacion_media = calcular_puntaje(puntajes_user1[0],puntajes_user1[1])
                    score = Score(lista[0],puntuacion_media)
                    if not score_saved:
                        score.save_data()
                        score_saved=True
                elif len(puntajes_user2)>1:
                    puntuacion_media = calcular_puntaje(puntajes_user2[0],puntajes_user2[1])
                    score = Score(lista[1],puntuacion_media)
                    if not score_saved:
                        score.save_data()
                        score_saved=True
                screen.blit(texto, (screen_width // 2 - texto.get_width() // 2, screen_height // 2 - texto.get_height() // 2))
                if ronda<3:
                    ronda = ronda+1
                    break
            elif tiempo_segundos>tiempo_defensa_defensor:
                puntos_defensor= len(obstaculos)
                if ronda==1:
                    texto = font.render("El defensor "+str(lista[0])+" ha ganado", True, (255, 255, 255))
                    puntajes_user1.append(puntos_defensor)
                elif ronda==2:
                    texto = font.render("El defensor "+str(lista[1])+" ha ganado", True, (255, 255, 255))
                    puntajes_user2.append(puntos_defensor)
                elif ronda==3:
                    texto = font.render("El defensor "+str(lista[0])+" ha ganado", True, (255, 255, 255))
                    puntajes_user1.append(puntos_defensor)

                if len(puntajes_user1)>1:
                    puntuacion_media = calcular_puntaje(puntajes_user1[0],puntajes_user1[1])
                    score = Score(lista[0],puntuacion_media)
                    if not score_saved:
                        score.save_data()
                        score_saved=True
                elif len(puntajes_user2)>1:
                    puntuacion_media = calcular_puntaje(puntajes_user2[0],puntajes_user2[1])
                    score = Score(lista[1],puntuacion_media)
                    if not score_saved:
                        score.save_data()
                        score_saved=True

                
                screen.blit(texto, (screen_width // 2 - texto.get_width() // 2, screen_height // 2 - texto.get_height() // 2))
                if ronda<3:
                    ronda = ronda+1
                    break
            if defensor_done:
                obstaculos.draw(screen)
                
                defensor.update()
                screen.blit(defensor.image, defensor.rect)
                
                    # Dibujar los proyectiles
                proyectiles.update()
                proyectiles.draw(screen)
                
            else:
                
                
                texto = font.render("Coloca el águila en un punto estrategico", True, (255, 255, 255))
                screen.blit(texto, (screen_width // 2 - texto.get_width() // 2, screen_height // 2 - texto.get_height() // 2))

            if obs_done:
                mirilla.update()
                todos_los_sprites.update()
                todos_los_sprites.draw(screen)
            elif defensor_done:
                
                tiempo_segundos = pygame.time.get_ticks() // 1000
                
                texto = font.render("Coloca los obstaculos iniciales", True, (255, 255, 255))
                screen.blit(texto, (screen_width // 2 - texto.get_width() // 2, screen_height // 2 - texto.get_height() // 2))

            frame_counter += 1
            if frame_counter >= animation_speed:
                
                frame_counter = 0  # Reiniciar el contador
                current_frame = (current_frame + 1) % 100
            # Calcular el tiempo en segundos transcurrido desde el inicio del juego
            

            # Mostrar el tiempo en la ventana del juego
            font = pygame.font.Font(None, 36)  # Fuente y tamaño del texto
            texto_tiempo = font.render("Tiempo: {} seg".format(tiempo_segundos), True, (255, 255, 255))  # Crear el texto
            screen.blit(texto_tiempo, (10, 10))  # Mostrar el texto en la ventana en la posición (10, 10)
            screen.blit(flagsprite2[current_frame%len(flagsprite2)], (screen_width // 8 - 32, screen_height //8*2 - screen_height//10))

            screen.blit(flagsprite2[current_frame%len(flagsprite2)], (screen_width // 8 - 32, screen_height //8*7 - screen_height//10))
            
            screen.blit(flagsprite1[current_frame%len(flagsprite1)], (screen_width // 8*7 - 32, screen_height //8*7 - screen_height//10))
            


            screen.blit(campfiresprite[current_frame%len(campfiresprite)], (screen_width // 22*21 - 32, screen_height // 8*2))
            screen.blit(campfiresprite[current_frame%len(campfiresprite)], (screen_width // 22*1.5 - 32, screen_height // 8*5.5))
            screen.blit(layer, (0, 45))
            screen.blit(powers_image, (screen_width - screen_width/8.5, screen_height // 2 - (screen_height/3.5)/3))
            screen.blit(selected_image_surface1, (WIDTH//2-750, HEIGHT//2-520))
            screen.blit(selected_image_surface2, (WIDTH//2+750, HEIGHT//2-520))
                # Dibujar los círculos en el lado derecho de la pantalla
            radio = 7  # Radio de los círculos
            espacio_entre_circulos = 7  # Espacio entre los círculos
            inicio_x = screen_width - screen_width/14

            for i in range(atacante.bolas_fuego):
                x = inicio_x + i * (2 * radio + espacio_entre_circulos)
                y = screen_height // 2 - (screen_height/20)/4 +radio# Ajustar según tus necesidades
                pygame.draw.circle(screen, circle_color, (x, y), radio)

            for i in range(atacante.bolas_agua):
                x = inicio_x + i * (2 * radio + espacio_entre_circulos)
                y = screen_height // 1.8 - (screen_height/20)/5+radio# Ajustar según tus necesidades
                pygame.draw.circle(screen, circle_color, (x, y), radio)
            for i in range(atacante.bolas_polvora):
                x = inicio_x + i * (2 * radio + espacio_entre_circulos)
                y = screen_height // 1.63 - (screen_height/20)/5+radio# Ajustar según tus necesidades
                pygame.draw.circle(screen, circle_color, (x, y), radio)
            round_text = "Ronda " + str(ronda)
            round_surface = TITLE_FONT.render(round_text, True, PCBUTTON)
            screen.blit(round_surface, round_rect)
            pygame.display.flip()
            clock.tick(75)
            # Crear un nuevo obstáculo si todos los obstáculos han sido destruidos
            if not obstaculos:
                nueva_posicion_x = pygame.display.get_surface().get_width() + obstaculo.rect.width
                nueva_posicion_y = pygame.display.get_surface().get_height() // 2
                obstaculo = Obstaculo(nueva_posicion_x, nueva_posicion_y)
                obstaculos.add(obstaculo)

        
    pygame.quit()


