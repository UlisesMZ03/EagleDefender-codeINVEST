import pygame
import pygame_gui

import re
import json
from usuarios import Usuario
import serial
import os
import threading
import pygame

import pygame_gui
from pygame.locals import *
import sys
import os


import shutil

pygame.init()

WIDTH, HEIGHT = 1280, 720

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Eagle Defender")

# Inicializar la cámara

manager = pygame_gui.UIManager((WIDTH, HEIGHT))

UID_device = None
FONT = pygame.font.Font(None, 30)
FONT_2 = pygame.font.Font(None, 25)
# En el área de inicialización del código
TITLE_FONT = pygame.font.Font(None, 64)  # Tamaño de la fuente para el título "Login"
# Dentro de la función login_screen() antes del bucle principal

background_image = pygame.image.load("images/bg2.jpg").convert()



selected_theme = None


BACKGROUND = '#005b4d'
PCBUTTON = '#01F0BF'
SCBUTTON = '#00A383'
TCBUTTOM = '#006350'

login_surface = TITLE_FONT.render("Login", True, PCBUTTON)  # Color blanco (#FFFFFF)
login_rect = login_surface.get_rect(center=(WIDTH // 2, 50))  # Ajusta las coordenadas según la posición que desees

or_surface = FONT.render("or", True, SCBUTTON)  # Color blanco (#FFFFFF)
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
					print('click')
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
                txt_surface = FONT.render(self.text, True, self.color)
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
                
                if event.key == pygame.K_BACKSPACE and self.cursor_pos > 0:
                    self.real_text = self.real_text[:self.cursor_pos - 1] + self.real_text[self.cursor_pos:]
                    self.cursor_pos -= 1
                    
                    self.text = self.real_text
                    
                elif event.key == pygame.K_DELETE and self.cursor_pos < len(self.text):
                    self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos + 1:]
                elif event.key == pygame.K_LEFT and self.cursor_pos > 0:
                    self.cursor_pos -= 1
                elif event.key == pygame.K_RIGHT and self.cursor_pos < len(self.text):
                    self.cursor_pos += 1
                elif event.key == pygame.K_RETURN:
                    self.active = False
                elif event.unicode.isalpha() or event.unicode.isdigit() or event.unicode in special_symbols:  # Permitir solo letras y números
                    # Mostrar el rombo si es una contraseña
                    char = '*' if self.is_password else event.unicode
                    self.text = self.text[:self.cursor_pos] + char + self.text[self.cursor_pos:]
                    self.real_text = self.real_text[:self.cursor_pos] + event.unicode + self.real_text[self.cursor_pos:]

                    self.cursor_pos += 1
    def get_text(self):
       
        return self.real_text
    def set_text(self, new_text):
      
        self.real_text = new_text
        self.text = new_text
        self.cursor_pos = len(new_text)

    def update(self,min_width):
        txt_surface = FONT.render(self.text, True, self.color)
        # Establece el ancho mínimo del campo de texto
        
        self.rect.w = max(min_width, txt_surface.get_width() + 10)
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, 2)
        if self.is_password:
            masked_text = '*' * len(self.real_text)
            txt_surface = FONT.render(masked_text if masked_text else self.placeholder, True, self.color)
        else:
            txt_surface = FONT.render(self.real_text if self.real_text else self.placeholder, True, self.color)
        surface.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))
        if self.active and self.text:  # Mostrar el cursor solo si el cuadro de texto está activo y tiene texto
            cursor_x = self.rect.x + 5 + FONT.render(self.text[:self.cursor_pos], True, self.color).get_width()
            pygame.draw.line(surface, self.color, (cursor_x, self.rect.y + 5),
                            (cursor_x, self.rect.y + 5 + txt_surface.get_height()), 2)




def login():
    # Obtiene los datos ingresados por el usuario
    username = username_input.text
    password = password_input.get_text()
    
    # Abre el archivo JSON y carga los datos en una lista de diccionarios
    with open("usuarios.json", "r") as json_file:
        data = json.load(json_file)
        
    # Busca el usuario en la lista de usuarios registrados
    for usuario_data in data:
        if usuario_data["Username"] == username and usuario_data["Password"] == password:
            mostrar_mensaje_error("Login Exitoso", "¡Bienvenido, {}!".format(username),PCBUTTON,SCBUTTON)
            # Aquí puedes agregar código para redirigir a la siguiente pantalla o realizar otras acciones
            break
    else:
        mostrar_mensaje_error("Error de Login", "Nombre de usuario o contraseña incorrectos",PCBUTTON,SCBUTTON)

    

def cargar_usuarios_desde_archivo():
    if os.path.exists("usuarios.json"):
        with open("usuarios.json", "r") as json_file:
            usuarios = json.load(json_file)
        return usuarios
    else:
        return []


        


def verificar_uid(UID_device):
    # Asegúrate de que UID_device tenga un valor
    if not UID_device:
        print("Error: UID_device no tiene un valor.")
        return
    
    # Abre el archivo JSON y carga los datos en una lista de diccionarios
    with open("usuarios.json", "r") as json_file:
        data = json.load(json_file)
        
    # Busca la dirección IP en la lista de usuarios registrados
    for usuario_data in data:
        if usuario_data["UID"] == UID_device:
            print("Dispositivo Encontrado")
            username_input.set_text(usuario_data["Username"])
            password_input.set_text(usuario_data["Password"])
            return usuario_data  # Retorna el diccionario del usuario si se encuentra
    
    # Si el UID no se encuentra
    print("Dispositivo no encontrado")
    return None  # Retorna None si el usuario no se encuentra






PANTALLA = pygame.display.set_mode((WIDTH, HEIGHT))

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

def draw_rounded_rectangle(surface, color, rect, radius, alpha=255):
    # Convierte el color hexadecimal a un objeto Color de Pygame
    color_obj = pygame.Color(color)
    # Establece el canal alfa del color
    color_obj.a = alpha
    # Crea una copia del rectángulo con los mismos valores y tipo, pero con los valores truncados a enteros
    rect = pygame.Rect(rect)
    # Dibuja el rectángulo con el color y el canal alfa especificados
    pygame.draw.rect(surface, color_obj, rect, border_radius=radius)

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
                        usuario = verificar_uid(UID_device)
                        print(usuario)
                        
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
    mostrar_mensaje_error('Error de conexion', "No se ha podido establecer conexion\n             Intentalo nuevamente", PCBUTTON, SCBUTTON)
    uart_thread.join()  # Esperar a que el hilo termine
    
    


#CREDENCIALES LOGIN

username_input = TextInputBox((WIDTH//60)*7, 250, (WIDTH//60)*10, 40,PCBUTTON,SCBUTTON, "Username")
password_input = TextInputBox((WIDTH//60)*7, 300, 200, 40,PCBUTTON,SCBUTTON, "Password",is_password=True)

olvido_texto = "¿Olvidó su contraseña?"
olvido_surface = FONT_2.render(olvido_texto, True, PCBUTTON)  # Color del texto clicqueable
olvido_rect = olvido_surface.get_rect(center=(WIDTH // 2, 400))  # Centra el texto en la pantalla


login_button = Button('Log in',300,40,((WIDTH//60)*8,360),5,SCBUTTON)
register_button = Button('Register ',300,40,((WIDTH//60)*8,450),5,SCBUTTON)



#############
#PHONE LOGIN


log_device_button = Button('Phone Login ',(WIDTH/60)*16,40,(((WIDTH/60)*37),450),5,SCBUTTON)

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
                    login()
                elif log_device_button.top_rect.collidepoint(mouse_pos):
                     receive_data_from_uart()
                elif olvido_rect.collidepoint(mouse_pos):
                    # Acción a realizar cuando el usuario hace clic en "¿Olvidó su contraseña?"
                    mostrar_mensaje_error("Recuperar Contraseña", "Por favor, contacte al soporte para recuperar su contraseña.", PCBUTTON, SCBUTTON)
                            

        win.fill(BACKGROUND)
        global background_image
        win.blit(background_image, (0, 0))
         # Dibujar el rectángulo detrás de los campos de texto y botones
        crear_rectangulo_redondeado(hex_to_rgb(TCBUTTOM),WIDTH/60*5, HEIGHT-(HEIGHT//4*3), (WIDTH//60)*20, HEIGHT-(HEIGHT//4*2),15,alpha=200 )  # Ajusta las coordenadas y dimensiones según sea necesario


       
        crear_rectangulo_redondeado(hex_to_rgb(TCBUTTOM),WIDTH/60*35, HEIGHT-(HEIGHT//4*3), (WIDTH//60)*20, HEIGHT-(HEIGHT//4*2),15,alpha=200 )
        crear_rectangulo_redondeado(hex_to_rgb(BACKGROUND),(WIDTH//60*25), 7, ((WIDTH//60)*11), (80),15,alpha=95)
        crear_rectangulo_redondeado(hex_to_rgb(BACKGROUND),-15, 0, (WIDTH+30), (HEIGHT),15,alpha=95)
   
        
        username_input.update((WIDTH/60)*16)
        password_input.update((WIDTH/60)*16)

        
        
        username_input.draw(win)
        password_input.draw(win)
        login_button.draw(PCBUTTON,SCBUTTON)
        register_button.draw(PCBUTTON,SCBUTTON)
        log_device_button.draw(PCBUTTON,SCBUTTON)
        
        
        # Actualizar pygame_gui
        manager.update(time_delta)
        manager.draw_ui(win)
        # Dentro del bucle principal de la función login_screen()
        login_surface = TITLE_FONT.render("Login", True, PCBUTTON)
        win.blit(login_surface, login_rect)

        or_surface = FONT.render("or", True, SCBUTTON)  # Color blanco (#FFFFFF)
        win.blit(or_surface,or_rect)
        
        olvido_surface = FONT_2.render(olvido_texto, True, PCBUTTON)  # Renderiza el texto nuevamente si cambia
        olvido_rect = olvido_surface.get_rect(center=(WIDTH//60*15,420))  # Actualiza las dimensiones del rectángulo según el texto
        win.blit(olvido_surface, olvido_rect.topleft) 

        
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    login_screen()

