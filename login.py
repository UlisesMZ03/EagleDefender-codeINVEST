import pygame
import pygame_gui

import re
import json
from objectbasedata import Usuario
from objectbasedata import Musica
import serial
import os
import threading
import pygame

import pygame_gui
from pygame.locals import *
import sys
import os
import gameWindow 
import register

import shutil
import pygame.mixer
pygame.mixer.init()

pygame.init()
pygame.mixer.music.load('sounds/login.mp3')
pygame.mixer.music.play(-1)  # El argumento -1 hace que la canción se reproduzca en un bucle infinito
screen_info = pygame.display.Info()
user_id='User_Icon'
# Configuración de la pantalla
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h


win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Eagle Defender")

# Inicializar la cámara

manager = pygame_gui.UIManager((WIDTH, HEIGHT))

UID_device = None
FONT = pygame.font.Font(None, 30)
    
FONT_2 = pygame.font.Font(None, 25)
# En el área de inicialización del código
TITLE_FONT =pygame.font.Font("font/KarmaFuture.ttf", 64)  # Tamaño de la fuente para el título "Login"
FONT = pygame.font.Font(pygame.font.match_font('dejavusans'), 20)
FONT_OR = pygame.font.Font("font/KarmaFuture.ttf", 20)
FONT_SEC = pygame.font.Font(pygame.font.match_font('dejavusans'), 20)
# Dentro de la función login_screen() antes del bucle principal
user_dev=None
background_image = pygame.image.load("images/bg2.jpg").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))


selected_theme = None


BACKGROUND = '#005b4d'
PCBUTTON = '#01F0BF'
SCBUTTON = '#00A383'
TCBUTTOM = '#006350'

login_surface = TITLE_FONT.render("Login", True, PCBUTTON)  # Color blanco (#FFFFFF)
login_rect = login_surface.get_rect(center=(WIDTH // 2, 50))  # Ajusta las coordenadas según la posición que desees

or_surface = FONT_OR.render("or", True, SCBUTTON)  # Color blanco (#FFFFFF)
or_rect = or_surface.get_rect(center=(WIDTH // 2, HEIGHT//2))  # Ajusta las coordenadas según la posición que desees

temas = ['Dark Green', 'Dark Red', 'Tema 3']

def cambiar_tema(selected_theme):
    global background_image
    global BACKGROUND, PCBUTTON, SCBUTTON, TCBUTTOM
    if selected_theme == 'Dark Green':

        background_image = pygame.image.load("images/bg2.jpg").convert()
        BACKGROUND = '#005b4d'
        PCBUTTON = '#01F0BF'
        SCBUTTON = '#00A383'
        TCBUTTOM = '#006350'
    elif selected_theme == 'Dark Red':

        background_image = pygame.image.load("images/bg.jpg").convert()
        BACKGROUND = '#140200'
        PCBUTTON = '#660A00'
        SCBUTTON = '#9C1000'
        TCBUTTOM = '#CF1500'
    

tema_dropdown = pygame_gui.elements.UIDropDownMenu(
    options_list=temas,
    starting_option=temas[0],
    relative_rect=pygame.Rect((100, 100), (100, 30)),
    manager=manager
)

muted = False

def toggle_mute():
    global muted
    pygame.mixer.music.set_volume(0 if muted else 1)  # Configura el volumen en 0 para silenciar y 1 para restaurar el volumen original
    muted = not muted  # Cambia el estado de silencio

class Button:
	def __init__(self,text,width,height,pos,elevation,color):
        
		#Core attributes 
		self.pressed = False
		self.elevation = elevation
		self.dynamic_elecation = elevation
		self.original_y_pos = pos[1]

		# top rectangle 
		self.top_rect = pygame.Rect(pos,(width,height))
		self.top_color = color

		# bottom rectangle 
		self.bottom_rect = pygame.Rect(pos,(width,height))
		self.bottom_color = color
        
		#text
		self.text_surf = FONT.render(text,True,'#FFFFFF')
          
		self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
        



	def draw(self,color,color2):
		# elevation logic 
        
		self.top_rect.y = self.original_y_pos - self.dynamic_elecation
		self.text_rect.center = self.top_rect.center 

		self.bottom_rect.midtop = self.top_rect.midtop
		self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

		pygame.draw.rect(win,self.bottom_color, self.bottom_rect,border_radius = 12)
		pygame.draw.rect(win,self.top_color, self.top_rect,border_radius = 12)
		win.blit(self.text_surf, self.text_rect)
		self.check_click(color,color2)
    



	def check_click(self, color,color2):
		mouse_pos = pygame.mouse.get_pos()
		if self.top_rect.collidepoint(mouse_pos):
			self.top_color = color2
            
			if pygame.mouse.get_pressed()[0]:
				self.dynamic_elecation = 0
				self.pressed = True
			else:
				self.dynamic_elecation = self.elevation
				if self.pressed == True:
					self.pressed = False
		else: 
			self.dynamic_elecation = self.elevation
			self.top_color = color
			self.bottom_color = color2
            
special_symbols = ['!', '@', '#', '$', '%', '&', '*', '+', '-', '=', '_', '?', '<', '>', '.', ',', ':', ';']
class TextInputBox:
    def __init__(self, x, y, width, height, color, color2, placeholder="", is_password=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = ""
        self.height=height
        self.width=width
        self.placeholder = placeholder
        self.active = False
        self.cursor_pos = 0  # Posición del cursor en el texto
        self.is_password = is_password  # Nuevo parámetro para indicar si es una contraseña
        self.real_text = ""  # Variable para almacenar el texto real

    def handle_event(self, event, color, color2):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                # Calcular la posición del cursor en función de la posición del clic
                click_x = event.pos[0] - (self.rect.x + 5)
                
                self.cursor_pos = len(self.text)
                txt_surface = FONT_SEC.render(self.text, True, self.color)
                for i in range(len(self.text)):
                    if txt_surface.get_width() > click_x:
                        self.cursor_pos = i
                        break
                    click_x -= txt_surface.subsurface((i, 0, 1, 1)).get_width()
            else:
                self.active = False
            self.color = color2 if self.active else color
        if event.type == pygame.KEYDOWN:
            if self.active:
                
                if event.key == pygame.K_BACKSPACE and self.cursor_pos > 0 and not self.is_password:
                    self.real_text = self.real_text[:self.cursor_pos - 1] + self.real_text[self.cursor_pos:]
                    self.cursor_pos -= 1
                    
                    self.text = self.real_text
                elif event.key == pygame.K_BACKSPACE and self.cursor_pos > 0 and self.is_password:
                    self.real_text = self.real_text[:self.cursor_pos - 1] + self.real_text[self.cursor_pos:]
                    self.cursor_pos -= 1
                    self.text = u'\u25C6' * len(self.real_text)

                elif event.key == pygame.K_DELETE and self.cursor_pos < len(self.text):
                    self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos + 1:]
                elif event.key == pygame.K_LEFT and self.cursor_pos > 0:
                    self.cursor_pos -= 1
                elif event.key == pygame.K_RIGHT and self.cursor_pos < len(self.text):
                    self.cursor_pos += 1
                elif event.key == pygame.K_RETURN:
                    self.active = False
                elif self.is_password==True and (event.unicode.isalpha() or event.unicode.isdigit() or event.unicode in special_symbols):  # Permitir solo letras y números
                    # Mostrar el rombo si es una contraseña
                    char = u'\u25C6' if self.is_password else event.unicode
                    self.text = self.text[:self.cursor_pos] + char + self.text[self.cursor_pos:]
                    self.real_text = self.real_text[:self.cursor_pos] + event.unicode + self.real_text[self.cursor_pos:]
                    self.cursor_pos += 1
                elif not self.is_password and (event.unicode.isalpha() or event.unicode.isdigit() or event.unicode.isspace() or event.key == pygame.K_TAB or event.unicode in special_symbols):
                    if event.key == pygame.K_TAB:
                        # Ignorar la tecla Tab
                        pass
                    else:
                        char = event.unicode
                        self.text = self.text[:self.cursor_pos] + char + self.text[self.cursor_pos:]
                        self.real_text = self.real_text[:self.cursor_pos] + char + self.real_text[self.cursor_pos:]
                        self.cursor_pos += 1



    def get_text(self):
        """
        Obtiene el texto real del TextInputBox, incluso si is_password es True.
        """
        return self.real_text
    def update(self):
        txt_surface = FONT_SEC.render(self.text, True, self.color)
        # Establece el ancho mínimo del campo de texto
        min_width = self.width
        self.rect.w = max(min_width, txt_surface.get_width() + 10)
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, 2)
        
        txt_surface = FONT_SEC.render(self.text if self.text else self.placeholder, True, self.color)
        surface.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))
        if self.active and self.text:  # Mostrar el cursor solo si el cuadro de texto está activo y tiene texto
            cursor_x = self.rect.x + 5 + FONT_SEC.render(self.text[:self.cursor_pos], True, self.color).get_width()
            pygame.draw.line(surface, self.color, (cursor_x, self.rect.y + 5),
                            (cursor_x, self.rect.y + 5 + txt_surface.get_height()), 2)
            
            
            
            





def loading_screen():
    loading_font = pygame.font.Font(None, 36)
    loading_text = loading_font.render("Loading...", True, (255, 255, 255))
    text_rect = loading_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        win.fill(BACKGROUND)
        win.blit(background_image, (0, 0))
        win.blit(loading_text, text_rect.topleft)
        pygame.display.flip()
        
        # Add loading logic here (loading resources, initializing game objects, etc.)
        # Once loading is complete, break out of the loop to proceed to the game window
        
        pygame.time.delay(1000)  # Simulate loading time (remove this line in your actual implementation)
        break


usuarios_autenticados= []
def login(mode):
    # Obtiene los datos ingresados por el usuario
    username = username_input.text
    password = password_input.get_text()
    
    # Abre el archivo JSON y carga los datos en una lista de diccionarios
    
    if Usuario.check_credentials(username,password) and mode==1:
        if len(usuarios_autenticados)>0:
            if username==usuarios_autenticados[0]:
                mostrar_mensaje_error("Error", "username logueado, {}!".format(username),PCBUTTON,SCBUTTON)
            else:
                mostrar_mensaje_error("Login Exitoso", "¡Bienvenido, {}!".format(username),PCBUTTON,SCBUTTON)
                print(user_dev)

                # Aquí puedes agregar código para redirigir a la siguiente pantalla o realizar otras acciones
            # Reemplaza 'otra_ventana' con el nombre real de tu script
                usuarios_autenticados.append(username)
                if len(usuarios_autenticados)==2:
                    pygame.mixer.music.pause()
                    loading_screen() 
                    gameWindow.game(usuarios_autenticados) 

                    pygame.quit()
                    sys.exit()
        else:
            
            mostrar_mensaje_error("Login Exitoso", "¡Bienvenido, {}!".format(username),PCBUTTON,SCBUTTON)
         
            usuarios_autenticados.append(username)
        
    else:
        if mode!=2:
            mostrar_mensaje_error("Error de Login", "Nombre de usuario o contraseña incorrectos",PCBUTTON,SCBUTTON)
    if user_dev!=None and mode==2:
        if len(usuarios_autenticados)>0:
            if user_dev['username']==usuarios_autenticados[0]:
                mostrar_mensaje_error("Error", "username logueado, {}!".format(user_dev['username']),PCBUTTON,SCBUTTON)
            else:
                mostrar_mensaje_error("Login Exitoso", "¡Bienvenido, {}!".format(username),PCBUTTON,SCBUTTON)
                print(user_dev)

                # Aquí puedes agregar código para redirigir a la siguiente pantalla o realizar otras acciones
            # Reemplaza 'otra_ventana' con el nombre real de tu script
                usuarios_autenticados.append(user_dev['username'])
                if len(usuarios_autenticados)==2:
                    pygame.mixer.music.pause()
                    loading_screen() 
                    gameWindow.game(usuarios_autenticados) 

                    pygame.quit()
                    sys.exit()
        else:
            
            mostrar_mensaje_error("Login Exitoso", "¡Bienvenido, {}!".format(user_dev['username']),PCBUTTON,SCBUTTON)
        
            usuarios_autenticados.append(user_dev['username'])
    else:
        if mode!=1:
            mostrar_mensaje_error("Error de Login", "Accede con tu dispositivo movil",PCBUTTON,SCBUTTON)

        








# Función para mostrar una ventana emergente con un mensaje de error
def mostrar_mensaje_error(title, mensaje, color, color2):
    # Llenar la pantalla con el color de fondo para eliminar el mensaje anterior
    win.fill(BACKGROUND)

    font_titulo = pygame.font.Font(None, 48)  # Fuente para el título, tamaño 48
    font_mensaje = pygame.font.Font(None, 36)  # Fuente para el mensaje, tamaño 36

    # Renderizar el título y el mensaje
    texto_titulo = font_titulo.render(title, True, color)
    texto_mensaje = font_mensaje.render(mensaje, True, color2)

    # Calcula las coordenadas para centrar el texto y el título
    titulo_x = (WIDTH - texto_titulo.get_width()) // 2
    titulo_y = HEIGHT // 3  # Posición vertical para el título (un cuarto de la pantalla)
    mensaje_x = (WIDTH - texto_mensaje.get_width()) // 2
    mensaje_y = titulo_y + texto_titulo.get_height() + 30  # Posición vertical para el mensaje (debajo del título con un espacio de 20 píxeles)

    # Dibujar el título y el mensaje en la pantalla
    win.blit(texto_titulo, (titulo_x, titulo_y))
    win.blit(texto_mensaje, (mensaje_x, mensaje_y))

    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
                esperando = False




server_socket = None



def crear_rectangulo_redondeado(color,x, y, width, height, radius, alpha):
    rectangulo = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Dibuja los bordes redondeados del rectángulo
    pygame.draw.rect(rectangulo, color + (alpha,), (radius, 0, width - 2*radius, height))
    pygame.draw.rect(rectangulo, color + (alpha,), (0, radius, width, height - 2*radius))
    
    # Dibuja las esquinas redondeadas
    pygame.draw.ellipse(rectangulo, color + (alpha,), (0, 0, 2*radius, 2*radius))
    pygame.draw.ellipse(rectangulo, color + (alpha,), (width - 2*radius, 0, 2*radius, 2*radius))
    pygame.draw.ellipse(rectangulo, color + (alpha,), (0, height - 2*radius, 2*radius, 2*radius))
    pygame.draw.ellipse(rectangulo, color + (alpha,), (width - 2*radius, height - 2*radius, 2*radius, 2*radius))
    
    win.blit(rectangulo, (x, y))

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))



def verificar_formato(data):
    patron = r"b'\d+'"
    if re.fullmatch(patron, data):
        return True
    else:
        return False
def receive_data_from_uart():
    def uart_thread_function():
        SERIAL_PORTS = ['/dev/ttyACM0', '/dev/ttyACM1', '/dev/ttyACM2']
        BAUD_RATE = 9600
        global hilo_en_ejecucion
        global UID_device
        
        for port in SERIAL_PORTS:
            try:
                ser = serial.Serial(port, BAUD_RATE)
                print(f"Conectado a {port}")
                hilo_en_ejecucion = True
                while hilo_en_ejecucion:
                    data_received = ser.readline().decode().strip()
                    print("Datos recibidos desde Raspberry Pi Pico:", data_received)
                    if data_received!='None' and verificar_formato(data_received):
                        hilo_en_ejecucion = False  # Detener el hilo si se recibe algún dato
                        global UID_device
                        UID_device = data_received
                        
                        
                    else:
                        # Si no se recibe ningún dato, continúa escuchando
                        pass
                break
                    
            except serial.SerialException:
                pass
        
        # El hilo se detendrá cuando salga del bucle for
    
    # Creamos un hilo para ejecutar uart_thread_function()
    uart_thread = threading.Thread(target=uart_thread_function)
    
    # Iniciamos el hilo
    
    uart_thread.start()
    while uart_thread.is_alive():  
        mostrar_mensaje_error('Esperando conexión...', "\nPara conectarte, accede a la red WiFi llamada EagleDefender\ny visita la dirección 192.168.4.1 desde tu navegador favorito", PCBUTTON, SCBUTTON)
    
    if UID_device is not None:
         mostrar_mensaje_error('Conexión establecida', "El ID asignado es:" + UID_device, PCBUTTON, SCBUTTON)
         global user_dev
         user_dev = Usuario.get_user_by_uid(UID_device)
         global user_id
         user_id = user_dev['id']
    else:
        mostrar_mensaje_error('Error de conexion', "No se ha podido establecer conexion\n             Intentalo nuevamente", PCBUTTON, SCBUTTON)
    uart_thread.join()  # Esperar a que el hilo termine
    
    


#CREDENCIALES LOGIN

username_input = TextInputBox((WIDTH//60)*7, HEIGHT//60*20, (WIDTH//60)*16, 40,PCBUTTON,SCBUTTON, "Username")
password_input = TextInputBox((WIDTH//60)*7, HEIGHT//60*20+50, (WIDTH//60)*16, 40,PCBUTTON,SCBUTTON, "Password",is_password=True)

olvido_texto = "¿Olvidó su contraseña?"
olvido_surface = FONT_2.render(olvido_texto, True, PCBUTTON)  # Color del texto clicqueable
olvido_rect = olvido_surface.get_rect(center=(WIDTH // 2, 400))  # Centra el texto en la pantalla


login_button = Button('Log in',(WIDTH/60)*16,40,((WIDTH//60)*7,HEIGHT//60*20+150),5,SCBUTTON)
login_devbutton = Button('Log in',(WIDTH/60)*16,40,((WIDTH/60)*37,HEIGHT//60*20+250),5,SCBUTTON)
register_button = Button('Register ',(WIDTH/60)*16,40,((WIDTH//60)*7,HEIGHT//60*20+200),5,SCBUTTON)



#############
#PHONE LOGIN

mute_button = Button('Mute', 100, 40, (20, 20), 5, SCBUTTON)

log_device_button = Button('Phone Login ',(WIDTH/60)*16,40,(((WIDTH/60)*37),HEIGHT//60*20+200),5,SCBUTTON)

def login_screen():
    running = True
    
    while running:
        time_delta = pygame.time.Clock().tick(60)/1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


            
            
            username_input.handle_event(event,PCBUTTON,SCBUTTON)
            password_input.handle_event(event,PCBUTTON,SCBUTTON)
            manager.process_events(event)
                        # Manejar eventos de pygame_gui

            if event.type == pygame.USEREVENT:
                        if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                            if event.text in temas:
                                cambiar_tema(event.text)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if login_button.top_rect.collidepoint(mouse_pos):
                    login(1)
                elif login_devbutton.top_rect.collidepoint(mouse_pos):
                    login(2)
                elif log_device_button.top_rect.collidepoint(mouse_pos):
                     receive_data_from_uart()
                elif olvido_rect.collidepoint(mouse_pos):
                    # Acción a realizar cuando el usuario hace clic en "¿Olvidó su contraseña?"
                    mostrar_mensaje_error("Recuperar Contraseña", "Por favor, contacte al soporte para recuperar su contraseña.", PCBUTTON, SCBUTTON)
                elif mute_button.top_rect.collidepoint(mouse_pos):
                     toggle_mute()
                elif register_button.top_rect.collidepoint(mouse_pos):
                    register.registration_screen() 
                    pygame.quit()
                    
                    sys.exit()
                            

        win.fill(BACKGROUND)
        global background_image
        win.blit(background_image, (0, 0))
         # Dibujar el rectángulo detrás de los campos de texto y botones
        crear_rectangulo_redondeado(hex_to_rgb(TCBUTTOM),WIDTH/60*5, HEIGHT-(HEIGHT//4*3), (WIDTH//60)*20, HEIGHT-(HEIGHT//4*2),15,alpha=200 )  # Ajusta las coordenadas y dimensiones según sea necesario


       
        crear_rectangulo_redondeado(hex_to_rgb(TCBUTTOM),WIDTH/60*35, HEIGHT-(HEIGHT//4*3), (WIDTH//60)*20, HEIGHT-(HEIGHT//4*2),15,alpha=200 )
        crear_rectangulo_redondeado(hex_to_rgb(BACKGROUND),(WIDTH//60*25), 7, ((WIDTH//60)*11), (80),15,alpha=95)
        crear_rectangulo_redondeado(hex_to_rgb(BACKGROUND),-15, 0, (WIDTH+30), (HEIGHT),15,alpha=95)

        
        username_input.update()
        password_input.update()

        
        username_input.draw(win)
        password_input.draw(win)
        login_button.draw(PCBUTTON,SCBUTTON)
        login_devbutton.draw(PCBUTTON,SCBUTTON)
        register_button.draw(PCBUTTON,SCBUTTON)
        log_device_button.draw(PCBUTTON,SCBUTTON)
        mute_button.draw(PCBUTTON,SCBUTTON)
        
        # Actualizar pygame_gui
        manager.update(time_delta)
        manager.draw_ui(win)
        # Dentro del bucle principal de la función login_screen()
        login_text = "User " + str(len(usuarios_autenticados)+1)
        login_surface = TITLE_FONT.render(login_text, True, PCBUTTON)
        win.blit(login_surface, login_rect)

        or_surface = FONT_OR.render("or", True, SCBUTTON)  # Color blanco (#FFFFFF)
        win.blit(or_surface,or_rect)
        
        olvido_surface = FONT_2.render(olvido_texto, True, PCBUTTON)  # Renderiza el texto nuevamente si cambia
        olvido_rect = olvido_surface.get_rect(center=(WIDTH//60*15,HEIGHT//60*20+100))  # Actualiza las dimensiones del rectángulo según el texto
        win.blit(olvido_surface, olvido_rect.topleft) 
        # Suponiendo que tengas el ID del usuario almacenado en una variable llamada 'user_id'
          # Reemplaza esto con el ID del usuario que deseas mostrar

        # Construir la ruta de la imagen usando el ID del usuario
        image_path = f"profile_photos/{user_id}.png"

        try:
            # Cargar la imagen
            original_image = pygame.image.load(image_path)

            # Redimensionar la imagen a 100x100 píxeles
            resized_image = pygame.transform.scale(original_image, (200, 200))

            # Calcular la posición para mostrar la imagen a la derecha de la pantalla
            image_x = (WIDTH/60)*42  # 50 píxeles de margen desde el borde derecho, considerando la nueva anchura de 100 píxeles
            image_y = HEIGHT//60*7+200  # Centrar verticalmente en la pantalla

            # Dibujar la imagen redimensionada en la pantalla
            win.blit(resized_image, (image_x, image_y))

        except pygame.error:
            # Si hay un error al cargar la imagen, puedes mostrar una imagen de error o manejarlo de otra manera
            print("Error al cargar o redimensionar la imagen:", image_path)

        
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    login_screen()

