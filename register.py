import pygame
import pygame_gui
import pygame.camera
import re
import json
import webbrowser
from usuarios import Usuario
import serial
import os
import threading
import pygame
import pygame.camera
import pygame_gui
from pygame.locals import *
import sys
import os
import pyautogui
import tkinter as tk
from tkinter import filedialog
from chooseMusic import list_music
import time


import shutil

pygame.init()
pygame.camera.init()
WIDTH, HEIGHT = 1280, 720

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Eagle Defender")

# Inicializar la cámara
camera = pygame.camera.Camera("/dev/video0", (WIDTH, HEIGHT))
camera.start()
manager = pygame_gui.UIManager((WIDTH, HEIGHT))
selected_image_surface = None
UID_device = None
FONT = pygame.font.Font(None, 30)
TITLE_FONT = pygame.font.Font(None,60)

selected_theme = None


BACKGROUND = '#005b4d'
PCBUTTON = '#01F0BF'
SCBUTTON = '#00A383'
TCBUTTOM = '#006350'
register_surface = TITLE_FONT.render("REGISTER", True, PCBUTTON)  # Color blanco (#FFFFFF)
register_rect = register_surface.get_rect(center=(WIDTH // 2, 50))  # Ajusta las coordenadas según la posición que desees

temas = ['Dark Green', 'Dark Red', 'Tema 3']

def cambiar_tema(selected_theme):
    global BACKGROUND, PCBUTTON, SCBUTTON, TCBUTTOM
    if selected_theme == 'Dark Green':
        BACKGROUND = '#005b4d'
        PCBUTTON = '#01F0BF'
        SCBUTTON = '#00A383'
        TCBUTTOM = '#006350'
    elif selected_theme == 'Dark Red':
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
# Configurar el rectángulo para la vista previa de la cámara
camera_preview_rect = pygame.Rect(700, 100, 300, 200)
camera_image = None  # Inicializar la imagen de la cámara fuera del bucle princUIDal


def load_selected_image(image_path):
    if os.path.exists(image_path):
        image_surface = pygame.image.load(image_path).convert()
        return pygame.transform.scale(image_surface, (camera_preview_rect.width, camera_preview_rect.height))
    return None


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
        



	def draw(self,color,color2,place):
		# elevation logic 
        
		self.top_rect.y = self.original_y_pos - self.dynamic_elecation
		self.text_rect.center = self.top_rect.center 

		self.bottom_rect.midtop = self.top_rect.midtop
		self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

		pygame.draw.rect(place,self.bottom_color, self.bottom_rect,border_radius = 12)
		pygame.draw.rect(place,self.top_color, self.top_rect,border_radius = 12)
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
        """
        Obtiene el texto real del TextInputBox, incluso si is_password es True.
        """
        return self.real_text
    def update(self):
        txt_surface = FONT.render(self.text, True, self.color)
        # Establece el ancho mínimo del campo de texto
        min_width = 300
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
            
    


def showMusic(set_music,favorite_song):
    scroll_offset = 0  # Desplazamiento de la lista de canciones
    song_display_limit = 1  # Número de canciones visibles a la vez
    font = pygame.font.Font(None, 30)
    text_color = (255, 255, 255)
    surfaceMusic=pygame.Surface((310,50))
    running = True
    while running:
        for event in pygame.event.get():
            #music_input.handle_event(event,PCBUTTON,SCBUTTON)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if scroll_offset > 0:
                        scroll_offset -= 1
                elif event.key == pygame.K_DOWN:
                    if scroll_offset < len(set_music) - song_display_limit:
                        scroll_offset += 1
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Verifica si el botón "Agregar" fue presionado
                if add_music_button.top_rect.collidepoint(event.pos):
                    if i < len(set_music):
                        if len(favorite_song)<3:
                            if set_music[i] in favorite_song:
                                print('ya has agregado la cancion anteriormente')
                            else:
                                favorite_song.append(set_music[i])
                                mostrar_mensaje_error("Canciones Favoritas", ' Has agregado la cancion ' + set_music[i]['name_song']+ ' de ' + set_music[i]['name_artist'] + 'a canciones favoritas' , PCBUTTON, SCBUTTON)
                                print(f"Se agregó la canción {set_music[i]['name_artist']} a favoritas")
                                running=False
                        
                        else:
                            running=False
                            mostrar_mensaje_error("Cantidad maxima de canciones alcanzada", 'Solo puedes agregar 3 Canciones', PCBUTTON, SCBUTTON)
                            print("solo puedes agregar 3 canciones")

        surfaceMusic.fill((BACKGROUND ))  # Limpia la pantalla

        y = 20  # Posición vertical inicial para la primera canción a mostrar
        # Dibuja las canciones en la pantalla
        for i in range(scroll_offset, min(scroll_offset + song_display_limit, len(set_music))):
            text = font.render(" Artista: " + set_music[i]['name_artist'], True, text_color)
            surfaceMusic.blit(text, (20, y))
            add_music_button = Button('Agregar',140,40,(100,450),5,SCBUTTON)
            
            add_music_button.draw(PCBUTTON,TCBUTTOM,surfaceMusic)
        
            #add_button = font.render("Agregar a favoritas", True, (0, 255, 0))
            #add_button_rect = add_button.get_rect()
            #add_button_rect.topleft = (200, y)
            #surfaceMusic.blit(add_button, add_button_rect)

            # Verifica si el botón "Agregar a canciones favoritas" fue presionado
          

        y += 50  # Espaciado entre canciones

        win.blit(surfaceMusic, (300, 450))

        pygame.display.flip()
    
    

    


def cargar_usuarios_desde_archivo():
    if os.path.exists("usuarios.json"):
        with open("usuarios.json", "r") as json_file:
            usuarios = json.load(json_file)
        return usuarios
    else:
        return []


def validar_datos_duplicados(username, email, UID):
    usuarios_existentes = cargar_usuarios_desde_archivo()
    for usuario in usuarios_existentes:
        if usuario["Username"] == username:
            return False, "Username already exists."
        if usuario["Email"] == email:
            return False, "Email already exists."
        if usuario["UID"] == UID:
            return False, "Mobile device is already linked to another account"
    return True, None


def validate_UID_device(UID_device):
    if not UID_device:
        return False
    
    # Verificar si la dirección UID consiste en grupos de enteros separados por puntos
    UID_parts = UID_device.split('.')
    if len(UID_parts) != 4:
        return False
    
    for part in UID_parts:
        if not part.isdigit() or not 0 <= int(part) <= 255:
            return False
    
    return True

def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)

def validate_password(password):
    password_regex = r'^(?=.*[A-Z])(?=.*[!@#$%^&*()_+{}\[\]:;<>,.?~\\-]).{8,}$'
    return re.match(password_regex, password)

def validate_username(username):
    banned_words = ['badword1', 'badword2', 'badword3']
    return all(word not in username.lower() for word in banned_words)

def validate_age(age):
    return age.isdigit()

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


# Función para el botón de registro
def register():
    name = name_input.text
    email = email_input.text
    age = age_input.text
    username = username_input.text
    password = password_input.get_text()
    print(password)
    confirm_password = confirm_password_input.get_text()

    if username != "" and password == confirm_password and validate_email(email) and validate_password(password) and validate_username(username) and validate_age(age) and UID_device!=None:
        
        # Validar si los datos ya existen en los usuarios registrados
        datos_validos, mensaje_error = validar_datos_duplicados(username, email, UID_device)
        
        if datos_validos:
            
            

            user = Usuario(name,username,age,email,UID_device,password)
            print(user)

            # Convertir el objeto de usuario a un diccionario
            user_dict = {
                "Name": name,
                "Username": username,
                "Email": email,
                "Age": age,
                "UID": UID_device,
                "Password": password
            }
            
                    # Verificar si el archivo usuarios.json existe
            if not os.path.exists("usuarios.json"):
                # Si no existe, crear un nuevo archivo y escribir el primer usuario
                with open("usuarios.json", "w") as json_file:
                    json.dump([user_dict], json_file, indent=4)
            else:
                # Si el archivo existe, abrirlo y agregar el nuevo usuario al final
                with open("usuarios.json", "r") as json_file:
                    
                    # Cargar datos existentes del archivo
                    users = json.load(json_file)
                # Agregar el nuevo usuario a la lista existente
                users.append(user_dict)
                # Escribir la lista actualizada al archivo
                with open("usuarios.json", "w") as json_file:
                    json.dump(users, json_file, indent=4)
        else:
            mostrar_mensaje_error("Registration Failed", mensaje_error, PCBUTTON, SCBUTTON)

    elif password != confirm_password:
        mostrar_mensaje_error('Password Mismatch','Password and confirm password do not match',PCBUTTON,SCBUTTON)
      
    elif not validate_email(email):
        mostrar_mensaje_error('Invalid Email','Please enter a valid email address',PCBUTTON,SCBUTTON)
    elif not validate_password(password):
        mostrar_mensaje_error('Invalid Password','Password must be at least 8 characters long with at least one uppercase letter and one special symbol',PCBUTTON,SCBUTTON)
       
    elif not validate_username(username):
        mostrar_mensaje_error('Invalid Username','Username contains prohibited words',PCBUTTON,SCBUTTON)
       
    elif not validate_age(age):
        mostrar_mensaje_error('Invalid Age','Age must be a number',PCBUTTON,SCBUTTON)
    elif UID_device==None:
         
        mostrar_mensaje_error('Add Device.',' You havent added the device or there has been an error. \nPlease try again',PCBUTTON,SCBUTTON)
    elif not verificar_formato(UID_device):
        mostrar_mensaje_error('Device error.',' You havent added the device or there has been an error. \nPlease try again',PCBUTTON,SCBUTTON)
        
    else:

        mostrar_mensaje_error('Register Failed','Invalid Username and password',PCBUTTON,SCBUTTON)


server_socket = None



# Variable de bandera para controlar la ejecución del hilo
hilo_en_ejecucion = True
def select_folder():
     file_path = filedialog.askopenfilename(filetypes=[("Archivos PNG", "*.png"), ("Archivos JPEG", "*.jpg")])
     if file_path:
        global selected_image_surface 
        selected_image_surface= load_selected_image(file_path)          
        # Carpeta donde se guardarán las imágenes con nuevos nombres
        output_folder = os.path.join("profile_photos")

        # Crea la carpeta "profile_photos" si no existe
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Nuevo nombre para la imagen (puedes cambiar esto según tus necesidades)
        new_image_name = "nuevo_nombre.png"

        # Ruta completa de la nueva imagen
        new_image_path = os.path.join(output_folder, new_image_name)

        # Copia y renombra la imagen seleccionada a la carpeta "profile_photos"
        shutil.copy(file_path, new_image_path)


def draw_rounded_rectangle(surface, color, rect, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)


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
                        # Detener el hilo si se recibe algún dato
                        UID_device = data_received
                        hilo_en_ejecucion = False  
                        
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
    mostrar_mensaje_error('Error de conexion', "No se ha podido establecer conexion\n            Intentalo nuevamente", PCBUTTON, SCBUTTON)
    uart_thread.join()  # Esperar a que el hilo termine
    
    




 

email_input = TextInputBox(300, 100, 200, 40,PCBUTTON,SCBUTTON, "Email")
name_input = TextInputBox(300, 150, 200, 40,PCBUTTON,SCBUTTON, "Name")
age_input = TextInputBox(300, 200, 200, 40,PCBUTTON,SCBUTTON, "Age")
username_input = TextInputBox(300, 250, 200, 40,PCBUTTON,SCBUTTON, "Username")
password_input = TextInputBox(300, 300, 200, 40,PCBUTTON,SCBUTTON, "Password",is_password=True)
confirm_password_input = TextInputBox(300, 350, 200, 40, PCBUTTON,SCBUTTON,"Confirm Password",is_password=True)
music_input = TextInputBox(300, 400,50, 40, PCBUTTON,SCBUTTON,"write the song")





register_button = Button('Register',140,40,(300,520),5,SCBUTTON)
add_device_button = Button('Add Device',140,40,(460,520),5,SCBUTTON)
take_foto_button = Button('Take foto',200,40,(750,350),5,SCBUTTON)
select_image_button = Button('select foto',200,40,(750,400),5,SCBUTTON)
reset_button = Button('reset',200,40,(750,450),5,SCBUTTON)
search_music_button = Button('look for',100,40,(620,400),5,SCBUTTON)
song_list=[]
favorite_song=[]

def registration_screen():
    global selected_image_surface
    running = True
    
    while running:
        time_delta = pygame.time.Clock().tick(60)/1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

           
            email_input.handle_event(event,PCBUTTON,SCBUTTON)
            age_input.handle_event(event,PCBUTTON,SCBUTTON)
            username_input.handle_event(event,PCBUTTON,SCBUTTON)
            password_input.handle_event(event,PCBUTTON,SCBUTTON)
            confirm_password_input.handle_event(event,PCBUTTON,SCBUTTON)
            name_input.handle_event(event,PCBUTTON,SCBUTTON)
            music_input.handle_event(event,PCBUTTON,SCBUTTON)
            manager.process_events(event)
                        # Manejar eventos de pygame_gui

            if event.type == pygame.USEREVENT:
                        if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                            if event.text in temas:
                                cambiar_tema(event.text)
            
            


            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if register_button.top_rect.collidepoint(mouse_pos):
                    register()
                elif add_device_button.top_rect.collidepoint(mouse_pos):
                     receive_data_from_uart()
                elif select_image_button.top_rect.collidepoint(mouse_pos):
                    file_dialog_thread = threading.Thread(target=select_folder)
                    file_dialog_thread.start()
                    
                elif search_music_button.top_rect.collidepoint(mouse_pos):
                    print(list_music(music_input.get_text()))
                    songs_list=list_music(music_input.get_text())
                    
                    showMusic(songs_list,favorite_song)
                    
                    
                elif take_foto_button.top_rect.collidepoint(mouse_pos):
                    image = camera.get_image()
                    camera_image = pygame.transform.scale(image, (camera_preview_rect.width, camera_preview_rect.height))
                    image_filename = os.path.join("profile_photos", "profile_photo.png")
                    pygame.image.save(camera_image, image_filename)
                    print(f"Foto guardada en: {image_filename}")
                    # Cambiar selected_image_surface para mostrar la última imagen capturada
                    selected_image_surface = camera_image
                elif reset_button.top_rect.collidepoint(mouse_pos):
                    # Restablecer el preview deseleccionando cualquier imagen
                    selected_image_surface = None
        


        
        email_input.update()
        age_input.update()
        username_input.update()
        password_input.update()
        confirm_password_input.update()
        name_input.update()
        music_input.update()

        win.fill(BACKGROUND)

        rect_dimensions = (WIDTH//6, 80, WIDTH-(WIDTH//6)*2, 500)  # Ajusta las coordenadas y dimensiones según sea necesario
        draw_rounded_rectangle(win, TCBUTTOM, rect_dimensions, 15)
        register_surface = TITLE_FONT.render("REGISTER", True, PCBUTTON)
        win.blit(register_surface, register_rect)
        email_input.draw(win)
        age_input.draw(win)
        username_input.draw(win)
        password_input.draw(win)
        confirm_password_input.draw(win)
        name_input.draw(win)
        music_input.draw(win)
        
        register_button.draw(PCBUTTON,TCBUTTOM,win)
        add_device_button.draw(PCBUTTON,TCBUTTOM,win)
        reset_button.draw(PCBUTTON,TCBUTTOM,win)
        select_image_button.draw(PCBUTTON,TCBUTTOM,win)
        take_foto_button.draw(PCBUTTON,TCBUTTOM,win)
        search_music_button.draw(PCBUTTON,TCBUTTOM,win)
        
        if selected_image_surface:
            win.blit(selected_image_surface, camera_preview_rect.topleft)
        else:
            image = camera.get_image()
            camera_image = pygame.transform.scale(image, (camera_preview_rect.width, camera_preview_rect.height))
            win.blit(camera_image, camera_preview_rect.topleft)

        # Actualizar pygame_gui
        manager.update(time_delta)
        manager.draw_ui(win)
   
        
        pygame.display.flip()

    camera.stop()
    pygame.quit()
    sys.exit()
    
    



if __name__ == "__main__":
    registration_screen()

