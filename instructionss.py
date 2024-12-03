import pygame
import pygame_gui

import re
import json
from objectbasedata import Usuario
from objectbasedata import Musica
from objectbasedata import Score
import serial
import os
import threading
import pygame
import menu
import pygame_gui
from pygame.locals import *
import sys
import os
import gameWindow 
import register
import login
import shutil
import pygame.mixer
pygame.mixer.init()

pygame.init()
pygame.mixer.music.load('sounds/login.mp3')
pygame.mixer.music.play(-1)  # El argumento -1 hace que la canción se reproduzca en un bucle infinito
screen_info = pygame.display.Info()

# Configuración de la pantalla
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h


win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Eagle Defender")

# Inicializar la cámara

manager = pygame_gui.UIManager((WIDTH, HEIGHT))

UID_device = None
FONT = pygame.font.Font(None, 30)
    
FONT_2 = pygame.font.Font(None, 28)
# En el área de inicialización del código
TITLE_FONT =pygame.font.Font("font/KarmaFuture.ttf", 64)  # Tamaño de la fuente para el título "Login"
FONT =pygame.font.Font("font/DejaVuSans.ttf", 20)
FONT_SUB_TITLE =pygame.font.Font("font/DejaVuSans-bOLD.ttf", 20)
FONT_OR = pygame.font.Font("font/KarmaFuture.ttf", 20)
FONT_SEC = pygame.font.Font(pygame.font.match_font('dejavusans'), 20)
# Dentro de la función instructions_screen() antes del bucle principal

background_image = pygame.image.load("images/bg2.jpg").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

instrucciones_img = pygame.image.load("images/game/instructions/fondo.png").convert_alpha()
instrucciones_img = pygame.transform.scale(instrucciones_img, (WIDTH/2+2*(WIDTH//4), HEIGHT//1.5))
selected_theme = None


BACKGROUND = '#005b4d'
PCBUTTON = '#01F0BF'
SCBUTTON = '#00A383'
TCBUTTOM = '#006350'

menu_surface = TITLE_FONT.render("Instrucciones", True, PCBUTTON)  # Color blanco (#FFFFFF)
menu_rect = menu_surface.get_rect(center=(WIDTH // 2, 50))  # Ajusta las coordenadas según la posición que desees

user_surface = FONT_SUB_TITLE.render("Player", True, PCBUTTON)  # Color blanco (#FFFFFF)
user_rect = user_surface.get_rect(center=(WIDTH /60*23, HEIGHT/4))

score_surface = FONT_SUB_TITLE.render("Score", True, PCBUTTON)  # Color blanco (#FFFFFF)
score_rect = score_surface.get_rect(center=(WIDTH /60*38, HEIGHT/4))


def cambiar_tema(selected_theme):
    global background_image
    global BACKGROUND, PCBUTTON, SCBUTTON, TCBUTTOM
    if selected_theme == 'Dark Green':

        background_image = pygame.image.load("images/bg2.jpg").convert()
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        BACKGROUND = '#005b4d'
        PCBUTTON = '#01F0BF'
        SCBUTTON = '#00A383'
        TCBUTTOM = '#006350'
    elif selected_theme == 'Dark Red':

        background_image = pygame.image.load("images/bg.jpg").convert()
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        BACKGROUND = '#140200'
        PCBUTTON = '#660A00'
        SCBUTTON = '#9C1000'
        TCBUTTOM = '#CF1500'
    



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




#############
#PHONE LOGIN

mute_button = Button('Mute', 100, 40,((WIDTH/20)*18,HEIGHT//20*18), 5, SCBUTTON)

menu_back_button = Button('BACK MENU',(WIDTH/60)*16,40,((WIDTH//2)-WIDTH/60*16/2,HEIGHT//60*50),5,SCBUTTON)




atacante_color = PCBUTTON
partida_color = SCBUTTON
defensor_color = PCBUTTON
puntaje_color = PCBUTTON
habilidades_color = PCBUTTON
poderes_color = PCBUTTON
        
puntaje_surface = FONT_SUB_TITLE.render("Puntaje", True, puntaje_color)
puntaje_rect = puntaje_surface.get_rect(center=(WIDTH /60*36, HEIGHT/4))  # Centra el texto en la pantalla

atacante_surface = FONT_SUB_TITLE.render("Atacante", True, atacante_color)  # Color del texto clicqueable
atacante_rect = atacante_surface.get_rect(center=(WIDTH /60*24, HEIGHT/4))  # Centra el texto en la pantalla

defensor_surface = FONT_SUB_TITLE.render("Defensor", True, defensor_color)  # Color del texto clicqueable
defensor_rect = defensor_surface.get_rect(center=(WIDTH /60*30, HEIGHT/4))  # Centra el texto en la pantalla

partida_surface = FONT_SUB_TITLE.render("Partida", True, partida_color)  # Color del texto clicqueable
partida_rect = partida_surface.get_rect(center=(WIDTH /60*18, HEIGHT/4))  # Centra el texto en la pantalla

habilidades_surface = FONT_SUB_TITLE.render("Habilidades", True, habilidades_color)  # Color del texto clicqueable
habilidades_rect = habilidades_surface.get_rect(center=(WIDTH /60*41.3, HEIGHT/4))  # Centra el texto en la pantalla

instructions_text = ("El juego Eagle Defender implica dos jugadores y dos partidas.\n" +
                    "En la primera, el defensor y el atacante se designan según el orden de  \n" +
                    "logueo. El defensor tiene un tiempo establecido para colocar bloques  \n" +
                    "en el tablero con el objetivo de proteger al águila, mientras que el  \n" +
                    "atacante intenta derribarla sin tocar los bloques. En la segunda partida,\n" +
                    "los roles se invierten. Si hay un empate (un ganador por cada jugador), \n" +
                    "se juega una tercera partida para decidir al ganador definitivo. El defensor \n" +
                    "gana al proteger el águila, evitando que sea derribada, mientras que el \n" +
                    "atacante gana al derribar el águila sin tocar los bloques de protección.\n" +
                    "¡A jugar!")



texto_surface = FONT_2.render(instructions_text, True, partida_color)  # Color del texto clicqueable
texto_rect = texto_surface.get_rect(center=(WIDTH /2, HEIGHT/2))  # Centra el texto en la pantalla





def instructions_screen():
    running = True
    global puntaje_color
    global partida_color
    global atacante_color
    global defensor_color
    global habilidades_color
    global instructions_text
    while running:
        time_delta = pygame.time.Clock().tick(60)/1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


            

            manager.process_events(event)
                        # Manejar eventos de pygame_gui



            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                if menu_back_button.top_rect.collidepoint(mouse_pos):
                    menu.loading_screen()
                    menu.menu_screen() 
                    pygame.quit()
                    
                    sys.exit()

                elif puntaje_rect.collidepoint(mouse_pos):
                     global instrucciones_img
                     instructions_text = ("")
                     instrucciones_img = pygame.image.load("images/game/instructions/puntaje.jpg").convert()
                     instrucciones_img = pygame.transform.scale(instrucciones_img, (WIDTH/2.2, HEIGHT//2.2))
                     puntaje_color = SCBUTTON
                     atacante_color = PCBUTTON
                     partida_color = PCBUTTON
                     defensor_color = PCBUTTON
                     habilidades_color = PCBUTTON
                elif partida_rect.collidepoint(mouse_pos):
                     instrucciones_img = pygame.image.load("images/game/instructions/fondo.png").convert_alpha()
                     instrucciones_img = pygame.transform.scale(instrucciones_img, (WIDTH/2.2, HEIGHT//2.2))
                     instructions_text = ("El juego Eagle Defender implica dos jugadores y dos partidas.\n" +
                    "En la primera, el defensor y el atacante se designan según el orden de  \n" +
                    "logueo. El defensor tiene un tiempo establecido para colocar bloques  \n" +
                    "en el tablero con el objetivo de proteger al águila, mientras que el  \n" +
                    "atacante intenta derribarla sin tocar los bloques. En la segunda partida,\n" +
                    "los roles se invierten. Si hay un empate (un ganador por cada jugador), \n" +
                    "se juega una tercera partida para decidir al ganador definitivo. El defensor \n" +
                    "gana al proteger el águila, evitando que sea derribada, mientras que el \n" +
                    "atacante gana al derribar el águila sin tocar los bloques de protección.\n" +
                    "¡A jugar!")

                     puntaje_color = PCBUTTON
                     atacante_color = PCBUTTON
                     partida_color = SCBUTTON
                     defensor_color = PCBUTTON
                     habilidades_color = PCBUTTON
                elif defensor_rect.collidepoint(mouse_pos):
                     
                     instructions_text = ("")
                     instrucciones_img = pygame.image.load("images/game/instructions/defensor.jpg").convert()
                     instrucciones_img = pygame.transform.scale(instrucciones_img, (WIDTH/2.2, HEIGHT//2.2))
              
                     puntaje_color = PCBUTTON
                     atacante_color = PCBUTTON
                     partida_color = PCBUTTON
                     defensor_color = SCBUTTON
                     habilidades_color = PCBUTTON
                elif atacante_rect.collidepoint(mouse_pos):
                     instructions_text = ("")
                     instrucciones_img = pygame.image.load("images/game/instructions/atacante.jpg").convert()
                     instrucciones_img = pygame.transform.scale(instrucciones_img, (WIDTH/2.2, HEIGHT//2.2))
                   
                     puntaje_color = PCBUTTON
                     atacante_color = SCBUTTON
                     partida_color = PCBUTTON
                     defensor_color = PCBUTTON
                     habilidades_color = PCBUTTON
                elif habilidades_rect.collidepoint(mouse_pos):
                     instructions_text = ("Habilidades")
                     puntaje_color = PCBUTTON
                     atacante_color = PCBUTTON
                     partida_color = PCBUTTON
                     defensor_color = PCBUTTON
                     habilidades_color = SCBUTTON
      
                elif mute_button.top_rect.collidepoint(mouse_pos):
                     toggle_mute()
    
                            

        win.fill(BACKGROUND)
        global background_image
        win.blit(background_image, (0, 0))
         # Dibujar el rectángulo detrás de los campos de texto y botones


       
        crear_rectangulo_redondeado(hex_to_rgb(TCBUTTOM),WIDTH/60*15, (HEIGHT//10)*2, (WIDTH//60)*30,(HEIGHT//10)*7,15,alpha=200 )
        crear_rectangulo_redondeado(hex_to_rgb(BACKGROUND),(WIDTH//60*20), 7, ((WIDTH//60)*20), (80),15,alpha=95)
        crear_rectangulo_redondeado(hex_to_rgb(BACKGROUND),-15, 0, (WIDTH+30), (HEIGHT),15,alpha=95)


        menu_back_button.draw(PCBUTTON,SCBUTTON)
        mute_button.draw(PCBUTTON,SCBUTTON)

        # Actualizar pygame_gui
        manager.update(time_delta)
        manager.draw_ui(win)
        # Dentro del bucle principal de la función instructions_screen()
        menu_surface = TITLE_FONT.render("Instrucciones", True, PCBUTTON)
        win.blit(menu_surface, menu_rect)
        win.blit(instrucciones_img,(WIDTH//3.61,HEIGHT//3))

        puntaje_surface = FONT_SUB_TITLE.render("Puntaje", True, puntaje_color)

        atacante_surface = FONT_SUB_TITLE.render("Atacante", True, atacante_color)  

        defensor_surface = FONT_SUB_TITLE.render("Defensor", True, defensor_color)  

        partida_surface = FONT_SUB_TITLE.render("Partida", True, partida_color)  

        habilidades_surface = FONT_SUB_TITLE.render("Habilidades", True, habilidades_color) 
        texto_surface = FONT_2.render(instructions_text, True, SCBUTTON) 

        win.blit(atacante_surface, atacante_rect.topleft) 
        win.blit(defensor_surface, defensor_rect.topleft)
        win.blit(partida_surface, partida_rect.topleft) 
        win.blit(puntaje_surface, puntaje_rect.topleft) 
        win.blit(habilidades_surface, habilidades_rect.topleft) 
        win.blit(texto_surface, texto_rect.topleft) 
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    instructions_screen()