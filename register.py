import pygame
import pygame_gui
import pygame.camera
import re
import login
#from usuarios import Usuario
import serial
import os
import threading
from pygame.locals import *
import sys
from tkinter import filedialog
from pygame.locals import *
import pyautogui
import shutil
from chooseMusic import list_music
from baseDatos import database
from objectbasedata import Usuario
from objectbasedata import Musica

pygame.init()
pygame.camera.init()
database()
screen_info = pygame.display.Info()

# Configuración de la pantalla
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h




win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Eagle Defender")

# Inicializar la cámara

# Obtiene la lista de cámaras disponibles
cameras = pygame.camera.list_cameras()

camera = None

# Itera sobre la lista de cámaras y trata de inicializar cada una
for cam in cameras:
    try:
        # Intenta inicializar la cámara actual
        camera = pygame.camera.Camera(cam, (WIDTH, HEIGHT))
        camera.start()  # Inicia la captura de la cámara
        break  # Si la inicialización fue exitosa, sal del bucle

    except pygame.error as e:
        # Si ocurre un error, imprímelo y pasa a la siguiente cámara
        print(f"Error al iniciar la cámara {cam}: {e}")

if camera:
    try:
        # Intenta capturar un fotograma
        frame = camera.get_image()

    

    except pygame.error as e:
        # Maneja errores al capturar el fotograma si es necesario
        print(f"Error al capturar el fotograma: {e}")

    finally:
        # Finaliza la captura de la cámara
        camera.stop()

else:
    # Si ninguna cámara pudo ser inicializada, imprime un mensaje
    print("No se pudo inicializar ninguna cámara.")
    
    camera=None
    pygame.camera.quit()



manager = pygame_gui.UIManager((WIDTH, HEIGHT))
selected_image_surface = None
camera_on = False
UID_device = None
FONT = pygame.font.Font(pygame.font.match_font('dejavusans'), 20)
TITLE_FONT = pygame.font.Font(None,60)
FONT_SEC = pygame.font.Font(pygame.font.match_font('dejavusans'), 20)
background_image = pygame.image.load("images/bg2.jpg").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

selected_theme = None


BACKGROUND = '#005b4d'
PCBUTTON = '#01F0BF'
SCBUTTON = '#00A383'
TCBUTTOM = '#006350'
register_surface = TITLE_FONT.render("REGISTER", True, PCBUTTON)  # Color blanco (#FFFFFF)
register_rect = register_surface.get_rect(center=(WIDTH // 2, 50))  # Ajusta las coordenadas según la posición que desees

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
image_pp = pygame.image.load("images/User_Icon.png").convert_alpha()
image_pp.fill(PCBUTTON, None, pygame.BLEND_MULT)
# Configurar el rectángulo para la vista previa de la cámara
camera_preview_rect = pygame.Rect(WIDTH/7*4, HEIGHT/14.4*3, WIDTH/7*2-55, HEIGHT/14.4*4)

camera_image = None  # Inicializar la imagen de la cámara fuera del bucle princUIDal
initial_image_surface = pygame.transform.scale(image_pp, (camera_preview_rect.width, camera_preview_rect.height))


profile_surface = pygame.Surface((camera_preview_rect.width, camera_preview_rect.height))
profile_surface.fill(SCBUTTON)


def load_selected_image(image_path):
    if os.path.exists(image_path):
        image_surface = pygame.image.load(image_path).convert()
        return pygame.transform.scale(image_surface, (camera_preview_rect.width, camera_preview_rect.height))
    return None


class Button:
    def __init__(self,text,width,height,pos,elevation,color):
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]
        self.width = width
        self.height = height
		#Core attributes 
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
    def update_button(self, new_text, new_size):
        # Actualizar el texto del botón
        self.text_surf = FONT.render(new_text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

        # Actualizar el tamaño del botón
        self.top_rect.width, self.top_rect.height = new_size
        self.bottom_rect.width, self.bottom_rect.height = new_size

            
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

    # Verificar si el nombre de usuario contiene espacios
    if ' ' in username:
        return 2
    # Verificar si el nombre de usuario contiene palabras prohibidas
    if any(word in username.lower() for word in banned_words):
        return 1
    # Si no hay espacios y no contiene palabras prohibidas, el nombre de usuario es válido
    return True

def validate_age(age):
    return age.isdigit()


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
    id_user = Usuario._get_next_id(Usuario)
    global favorite_song
    global selected_image_surface
    name = name_input.text
    email = email_input.text
    age = age_input.text
    username = username_input.text
    password = password_input.get_text()
    songs=favorite_song

    confirm_password = confirm_password_input.get_text()
    global UID_device
    
    if username != "" and password == confirm_password and validate_email(email) and validate_password(password) and validate_username(username) and validate_age(age) and selected_image_surface!=initial_image_surface:
        
        if UID_device == None:
            new_img_path = 'profile_photos/'+str(id_user)+'.png'
            if temp_file_path!=new_img_path:

                shutil.copy(temp_file_path, new_img_path)
            user = Usuario(name,username,age,email,password,"")
            validacion=user.save_to_db()
            if validacion==1:
                mostrar_mensaje_error('Username Already in Use', 'This username is already taken. Please choose another one.',PCBUTTON,SCBUTTON)
                
            elif validacion==2:
                mostrar_mensaje_error('Username Already in Use', 'This username is already taken. Please choose another one.',PCBUTTON,SCBUTTON)
            
            elif validacion!=1 and validacion!=2 and songs !=[]:
                user.save_to_db()
               
             
                print("entro al for")
                for i in songs:
                    musica_user=Musica(id_user,i["name_song"],i['name_artist'],i['url'])
                    musica_validacion= musica_user.save_data()
                    if musica_validacion:
                        favorite_song=[]
            
        else:
            user = Usuario(name,username,age,email,password,UID_device)
            validacion=user.save_to_db()
            if validacion==1:
                mostrar_mensaje_error('Username Already in Use', 'This username is already taken. Please choose another one.',PCBUTTON,SCBUTTON)
                
            elif validacion==2:
                mostrar_mensaje_error('Username Already in Use', 'This username is already taken. Please choose another one.',PCBUTTON,SCBUTTON)
            elif validacion==3:
                mostrar_mensaje_error('Device Already Linked', 'This device is already linked to another account. Please use a different device or contact support for assistance.',PCBUTTON,SCBUTTON)
            
            else:

                new_img_path = 'profile_photos/'+str(id_user)+'.png'
                if temp_file_path!=new_img_path:

                    shutil.copy(temp_file_path, new_img_path)
                user.save_to_db()
                login.login_screen() 

                pygame.quit()
                sys.exit()
     
    elif password != confirm_password:
        mostrar_mensaje_error('Password Mismatch','Password and confirm password do not match',PCBUTTON,SCBUTTON)
      
    elif not validate_email(email):
        mostrar_mensaje_error('Invalid Email','Please enter a valid email address',PCBUTTON,SCBUTTON)
    elif not validate_password(password):
        mostrar_mensaje_error('Invalid Password','Password must be at least 8 characters long with at least one uppercase letter and one special symbol',PCBUTTON,SCBUTTON)
    elif selected_image_surface==initial_image_surface:
        mostrar_mensaje_error('Registration Failed', 'You must add a profile picture', PCBUTTON, SCBUTTON)

    elif validate_username(username)==1:
        mostrar_mensaje_error('Invalid Username','Username contains prohibited words',PCBUTTON,SCBUTTON)
    elif validate_username(username)==2:
        mostrar_mensaje_error('Invalid Username','Username cannot contain spaces.',PCBUTTON,SCBUTTON)

    elif not validate_age(age):
        mostrar_mensaje_error('Invalid Profile Picture','You must upload or take a profile picture', PCBUTTON, SCBUTTON)

    elif not selected_image_surface:
        mostrar_mensaje_error('','Age must be a number',PCBUTTON,SCBUTTON)
    elif UID_device==None:
         
        mostrar_mensaje_error('Add Device.',' You havent added the device or there has been an error. \nPlease try again',PCBUTTON,SCBUTTON)
    elif not verificar_formato(UID_device):
        mostrar_mensaje_error('Device error.',' You havent added the device or there has been an error. \nPlease try again',PCBUTTON,SCBUTTON)
        
    


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

        name_photo = Usuario._get_next_id(Usuario)
        # Nuevo nombre para la imagen (puedes cambiar esto según tus necesidades)
        global temp_file_path
        new_image_name = str(name_photo)+".png"
 
       
        # Ruta completa de la nueva imagen
        temp_file_path = os.path.join(output_folder, new_image_name)

        # Copia y renombra la imagen seleccionada a la carpeta "profile_photos"
        shutil.copy(file_path, temp_file_path)



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

        # Puertos serie para Linux y Windows
        SERIAL_PORTS = []

        # Puertos serie en Linux
        linux_serial_ports = ['/dev/ttyACM0', '/dev/ttyACM1', '/dev/ttyACM2', '/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyS0', '/dev/ttyS1']

        # Puertos serie en Windows (los nombres pueden variar)
        windows_serial_ports = ['COM1', 'COM2', 'COM3', 'COM4']

        # Agregar puertos serie de Linux a la lista
        SERIAL_PORTS.extend(linux_serial_ports)

        # Agregar puertos serie de Windows a la lista
        SERIAL_PORTS.extend(windows_serial_ports)

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

    else:
        mostrar_mensaje_error('Error de conexion', "No se ha podido establecer conexion\n Intentalo nuevamente", PCBUTTON, SCBUTTON)
    uart_thread.join()  # Esperar a que el hilo termine
    



 

email_input = TextInputBox(WIDTH/7, HEIGHT/14.4*3, WIDTH/7*2, 40,PCBUTTON,SCBUTTON, "Email")
name_input = TextInputBox(WIDTH/7, HEIGHT/14.4*4, WIDTH/7*2, 40,PCBUTTON,SCBUTTON, "Name")
age_input = TextInputBox(WIDTH/7, HEIGHT/14.4*5, WIDTH/7*2, 40,PCBUTTON,SCBUTTON, "Age")
username_input = TextInputBox(WIDTH/7, HEIGHT/14.4*6, WIDTH/7*2, 40,PCBUTTON,SCBUTTON, "Username")
password_input = TextInputBox(WIDTH/7, HEIGHT/14.4*7, WIDTH/7*2, 40,PCBUTTON,SCBUTTON, "Password",is_password=True)
confirm_password_input = TextInputBox(WIDTH/7, HEIGHT/14.4*8, WIDTH/7*2, 40, PCBUTTON,SCBUTTON,"Confirm Password",is_password=True)
music_input = TextInputBox(WIDTH/7, HEIGHT/14.4*9, WIDTH/7*2, 40, PCBUTTON,SCBUTTON,"write the song (optional)")




register_button = Button('Register',WIDTH/7,40,(WIDTH/7*3,HEIGHT/14.4*11.3+50),5,SCBUTTON)
add_device_button = Button('Add Device (optional)',WIDTH/7*2,40,(WIDTH/7,HEIGHT/14.4*11),5,SCBUTTON)
take_foto_button = Button(u'\u25c9',50,40,(WIDTH/7*6-50,HEIGHT/14.4*3+10),5,SCBUTTON)
select_image_button = Button(u'\u2191',50,40,(WIDTH/7*6-50,HEIGHT/14.4*4+5),5,SCBUTTON)
reset_button = Button(u'\u2716',50,40,(WIDTH/7*6-50,HEIGHT/14.4*6+5),5,SCBUTTON)
search_music_button = Button("Search",WIDTH/15,40,(WIDTH/7*2.071+WIDTH/15,HEIGHT/14.4*9+5),5,SCBUTTON)
add_music_button = Button('Add',WIDTH/17,40,(WIDTH/7*2.071+WIDTH/17,HEIGHT/14.4*10),5,SCBUTTON)

       

favorite_song=[]
def registration_screen():
    global selected_image_surface
    global camera_on
    global initial_image_surface
    global background_image
    global favorite_song 
    global add_music_button
    
    scroll_offset = 0  # Desplazamiento de la lista de canciones
    song_display_limit = 1  # Número de canciones visibles a la vez
    font = pygame.font.Font(None, 30)
    text_color = (255, 255, 255)
    surfaceMusic=pygame.Surface((WIDTH/6,40))
    
    set_music=[]

   
    running = True
    selected_image_surface = initial_image_surface  # Establecer la imagen inicial
    profile_surface.blit(selected_image_surface, (0, 0))
    while running:
        win.fill(BACKGROUND)
        win.blit(background_image, (0, 0))
        time_delta = pygame.time.Clock().tick(60)/1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()


            
            
            email_input.handle_event(event,PCBUTTON,SCBUTTON)
            age_input.handle_event(event,PCBUTTON,SCBUTTON)
            username_input.handle_event(event,PCBUTTON,SCBUTTON)
            password_input.handle_event(event,PCBUTTON,SCBUTTON)
            confirm_password_input.handle_event(event,PCBUTTON,SCBUTTON)
            name_input.handle_event(event,PCBUTTON,SCBUTTON)
            music_input.handle_event(event,PCBUTTON,SCBUTTON)
            manager.process_events(event)
                        # Manejar eventos de pygame_gui
           
            #eventos de la musica
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
                                mostrar_mensaje_error("Canciones Favoritas", ' ya has agregado la canción anteriormente ' + set_music[i]['name_song']+ ' de ' + set_music[i]['name_artist'] + 'a canciones favoritas' , PCBUTTON, SCBUTTON)
                                break
                            else:
                                favorite_song.append(set_music[i])
                                print(f"Se agregó la canción {set_music[i]['name_artist']} a favoritas") 
                                mostrar_mensaje_error("Canciones Favoritas", ' Has agregado la cancion ' + set_music[i]['name_song']+ ' de ' + set_music[i]['name_artist'] + 'a canciones favoritas' , PCBUTTON, SCBUTTON)
                                break
                        else:
                           
                            mostrar_mensaje_error("Cantidad maxima de canciones alcanzada", 'Solo puedes agregar 3 Canciones', PCBUTTON, SCBUTTON)
                            print("solo puedes agregar 3 canciones")
                            print(f'canciones favoritas{favorite_song}')
                            break
                   


            if event.type == pygame.USEREVENT:
                        if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                            if event.text in temas:
                                cambiar_tema(event.text)
                                profile_surface.fill(SCBUTTON)
                                image_pp.fill(PCBUTTON, None, pygame.BLEND_MULT)
                                
                                if selected_image_surface==initial_image_surface:
                                    
                                    initial_image_surface=pygame.transform.scale(image_pp, (camera_preview_rect.width, camera_preview_rect.height))
                                    
                                    profile_surface.blit(initial_image_surface, (0, 0))
                                else:
                                    profile_surface.blit(selected_image_surface, (0, 0))

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if register_button.top_rect.collidepoint(mouse_pos):
                    register()
                elif add_device_button.top_rect.collidepoint(mouse_pos):
                     receive_data_from_uart()
                elif select_image_button.top_rect.collidepoint(mouse_pos):
                    if camera:
                        if camera_on:
                            camera.stop()
                            camera_on=False
                    if selected_image_surface==None:
                        initial_image_surface=pygame.transform.scale(image_pp, (camera_preview_rect.width, camera_preview_rect.height))
                                    
                        selected_image_surface= initial_image_surface
                    file_dialog_thread = threading.Thread(target=select_folder)
                    file_dialog_thread.start()
                
                elif take_foto_button.top_rect.collidepoint(mouse_pos):
                    if camera:
                        if not camera_on:
                            take_foto_button.update_button('[\u25c9"]',(50,40))
                            selected_image_surface = None
                            camera.start()
                            camera_on=True
                        else:
                            global tipo_img
                            tipo_img =1
                            take_foto_button.update_button('\u25c9',(50,40))
                            if not os.path.exists('profile_photos'):
                                os.makedirs('profile_photos')
                            image = camera.get_image()
                            global camera_image
                            camera_image = pygame.transform.scale(image, (camera_preview_rect.width, camera_preview_rect.height))
                            name_photo = Usuario._get_next_id(Usuario)
                            global temp_file_path
                            temp_file_path = os.path.join("profile_photos", str(name_photo)+".png")
                            pygame.image.save(camera_image, temp_file_path)
                            print(f"Foto guardada en: {temp_file_path}")
                            # Cambiar selected_image_surface para mostrar la última imagen capturada
                            selected_image_surface = camera_image
                            camera.stop()  # Detener la cámara después de tomar la foto
                            camera_on=False
                elif reset_button.top_rect.collidepoint(mouse_pos):
                    if camera:
                        if camera_on:
                            camera.stop()
                            camera_on=False
                        camera.start()
                        selected_image_surface = initial_image_surface  # Restablecer la imagen al valor inicial


                    
                elif search_music_button.top_rect.collidepoint(mouse_pos):
                    try:
                        set_music=list_music(music_input.get_text())
                       
                    except:
                        mostrar_mensaje_error("Canciones Favoritas", 'Escribe la canción para poder mostrarte los resultados' , PCBUTTON, SCBUTTON)
    



        surfaceMusic.fill((BACKGROUND ))  # Limpia la pantalla

        y = 20  # Posición vertical inicial para la primera canción a mostrar
        # Dibuja las canciones en la pantalla
        for i in range(scroll_offset, min(scroll_offset + song_display_limit, len(set_music))):

            text = font.render("Artista: " + set_music[i]['name_artist'], True, text_color)
            surfaceMusic.blit(text, (20, 10))
            
        y += 50  # Espaciado entre canciones
        #win.blit(surfaceMusic, (WIDTH/7,HEIGHT/14.4*10))
        
        email_input.update()
        age_input.update()
        username_input.update()
        password_input.update()
        confirm_password_input.update()
        name_input.update()
        music_input.update()

       

     
       

         # Ajusta las coordenadas y dimensiones según sea necesario
        crear_rectangulo_redondeado(hex_to_rgb(TCBUTTOM),WIDTH/7-10, HEIGHT/14.4*3-10, WIDTH/7*5+20, HEIGHT/14.4*8,15,alpha=200 )  # Ajusta las coordenadas y dimensiones según sea necesario
        crear_rectangulo_redondeado(hex_to_rgb(BACKGROUND),(WIDTH//60*25), 7, ((WIDTH//60)*11), (80),15,alpha=95)
        #draw_rounded_rectangle(win, TCBUTTOM, rect_dimensions, 15)
        register_surface = TITLE_FONT.render("REGISTER", True, PCBUTTON)
        win.blit(register_surface, register_rect)
        email_input.draw(win)
        age_input.draw(win)
        username_input.draw(win)
        password_input.draw(win)
        confirm_password_input.draw(win)
        name_input.draw(win)
        register_button.draw(PCBUTTON,TCBUTTOM)
        add_device_button.draw(PCBUTTON,TCBUTTOM)
        reset_button.draw(PCBUTTON,TCBUTTOM)
        select_image_button.draw(PCBUTTON,TCBUTTOM)
        take_foto_button.draw(PCBUTTON,TCBUTTOM)
        search_music_button.draw(PCBUTTON,TCBUTTOM)
        music_input.draw(win)
        win.blit(surfaceMusic, (WIDTH/7,HEIGHT/14.4*10))
        if len(set_music)>0:
                add_music_button.draw(PCBUTTON,TCBUTTOM)


        if selected_image_surface:
            if (selected_image_surface==initial_image_surface) :
                win.blit(profile_surface, (camera_preview_rect.x, camera_preview_rect.y))
            else:
                win.blit(selected_image_surface, (camera_preview_rect.x, camera_preview_rect.y))

        else:
            if camera_on:
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

