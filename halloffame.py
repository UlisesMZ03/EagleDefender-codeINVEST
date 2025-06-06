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
    
FONT_2 = pygame.font.Font(None, 25)
# En el área de inicialización del código
TITLE_FONT =pygame.font.Font("font/KarmaFuture.ttf", 64)  # Tamaño de la fuente para el título "Login"
FONT =pygame.font.Font("font/DejaVuSans.ttf", 20)
FONT_SUB_TITLE =pygame.font.Font("font/DejaVuSans-bOLD.ttf", 30)
FONT_OR = pygame.font.Font("font/KarmaFuture.ttf", 20)
FONT_SEC = pygame.font.Font(pygame.font.match_font('dejavusans'), 20)
# Dentro de la función hall_of_fame_screen() antes del bucle principal

background_image = pygame.image.load("images/bg2.jpg").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))


selected_theme = None


BACKGROUND = '#005b4d'
PCBUTTON = '#01F0BF'
SCBUTTON = '#00A383'
TCBUTTOM = '#006350'

menu_surface = TITLE_FONT.render("Hall of Fame", True, PCBUTTON)  # Color blanco (#FFFFFF)
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

def hall_of_fame_screen():
    running = True
    
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
               
                elif mute_button.top_rect.collidepoint(mouse_pos):
                     toggle_mute()
    
                            

        win.fill(BACKGROUND)
        global background_image
        win.blit(background_image, (0, 0))
         # Dibujar el rectángulo detrás de los campos de texto y botones


       
        crear_rectangulo_redondeado(hex_to_rgb(TCBUTTOM),WIDTH/60*15, (HEIGHT//10)*2, (WIDTH//60)*30,(HEIGHT//10)*7,15,alpha=200 )
        crear_rectangulo_redondeado(hex_to_rgb(BACKGROUND),(WIDTH//60*20), 7, ((WIDTH//60)*20), (80),15,alpha=95)
        crear_rectangulo_redondeado(hex_to_rgb(BACKGROUND),-15, 0, (WIDTH+30), (HEIGHT),15,alpha=95)
        # ... (código previo) ...

        # En el área de inicialización del código
        line_positions = [(WIDTH//60)*15, (HEIGHT//20)*6, (WIDTH//60)*45, (HEIGHT//20)*6,
                        (WIDTH//60)*15, (HEIGHT//20)*7, (WIDTH//60)*45, (HEIGHT//20)*7,
                        (WIDTH//60)*15, (HEIGHT//20)*8, (WIDTH//60)*45, (HEIGHT//20)*8,
                        (WIDTH//60)*15, (HEIGHT//20)*9, (WIDTH//60)*45, (HEIGHT//20)*9,
                        (WIDTH//60)*15, (HEIGHT//20)*10, (WIDTH//60)*45, (HEIGHT//20)*10,
                        (WIDTH//60)*15, (HEIGHT//20)*11, (WIDTH//60)*45, (HEIGHT//20)*11,
                        (WIDTH//60)*15, (HEIGHT//20)*12, (WIDTH//60)*45, (HEIGHT//20)*12,
                        (WIDTH//60)*15, (HEIGHT//20)*13, (WIDTH//60)*45, (HEIGHT//20)*13,
                        (WIDTH//60)*15, (HEIGHT//20)*14, (WIDTH//60)*45, (HEIGHT//20)*14,
                        (WIDTH//60)*15, (HEIGHT//20)*15, (WIDTH//60)*45, (HEIGHT//20)*15,
                        (WIDTH//60)*15, (HEIGHT//20)*16, (WIDTH//60)*45, (HEIGHT//20)*16]

        for i in range(0, len(line_positions), 4):
            pygame.draw.line(win, PCBUTTON, (line_positions[i], line_positions[i+1]), (line_positions[i+2], line_positions[i+3]), 2)

        # ... (resto del código) ...

        # Después de crear instancias de la clase Score y guardar los puntajes en la base de datos

        top_scores = Score.get_top_scores()

        # Ahora `top_scores` contendrá una lista con los 10 mejores puntajes y los IDs de los usuarios correspondientes.
        print("Top 10 Puntajes:")
        for id_user, puntaje in top_scores:
            print(f"ID Usuario: {id_user}, Puntaje: {puntaje}")

        # Después de obtener los top_scores de la base de datos
        top_scores = Score.get_top_scores()

        # Ahora `top_scores` contendrá una lista con los 10 mejores puntajes y los IDs de los usuarios correspondientes.

        # Calcular la posición inicial para mostrar los puntajes
        x_pos_user = (WIDTH // 60) * 23
        x_pos_score = (WIDTH // 60) * 38
        y_pos = (HEIGHT//40)*13

        # Renderizar y mostrar los 10 mejores puntajes en la ventana
        for i, (id_user, puntaje) in enumerate(top_scores[:10]):  # Mostrar solo los primeros 10 puntajes
            user_text = FONT.render(f"{id_user}", True, PCBUTTON)
            puntaje_redondeado = round(puntaje, 3)
            score_text = FONT.render(f"{puntaje_redondeado}", True, PCBUTTON)


            user_rect2 = user_text.get_rect(center=(x_pos_user, y_pos + i * (HEIGHT//40)*2))  # Espaciar los puntajes por 40 píxeles
            score_rect2 = score_text.get_rect(center=(x_pos_score, y_pos + i * (HEIGHT//40)*2))  # Espaciar los puntajes por 40 píxeles

            win.blit(user_text, user_rect2.topleft)
            win.blit(score_text, score_rect2.topleft)


        menu_back_button.draw(PCBUTTON,SCBUTTON)
        mute_button.draw(PCBUTTON,SCBUTTON)

        # Actualizar pygame_gui
        manager.update(time_delta)
        manager.draw_ui(win)
        # Dentro del bucle principal de la función hall_of_fame_screen()
        menu_surface = TITLE_FONT.render("Hall of Fame", True, PCBUTTON)
        win.blit(menu_surface, menu_rect)
        win.blit(score_surface, score_rect)
        win.blit(user_surface, user_rect)
     

        
        pygame.display.flip()

    pygame.quit()
    sys.exit()

