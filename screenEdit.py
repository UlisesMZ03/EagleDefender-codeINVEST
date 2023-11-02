import pygame
import pygame_gui
from TextInputBox import TextInputBox
import sys
from objectbasedata import Usuario, Musica
def editScreen():
    pygame.init()
    screen_info = pygame.display.Info()

# Configuración de la pantalla
    WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
    
    BACKGROUND = '#005b4d'
    PCBUTTON = '#01F0BF'
    SCBUTTON = '#00A383'
    TCBUTTOM = '#006350'

    win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Eagle Defender")

    manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    selected_image_surface = None
    camera_on = False
    UID_device = None
    FONT = pygame.font.Font(pygame.font.match_font('dejavusans'), 20)
    TITLE_FONT = pygame.font.Font(None,60)
    TITLE_DATA = pygame.font.Font(None,20)
    FONT_SEC = pygame.font.Font(pygame.font.match_font('dejavusans'), 20)   
    background_image = pygame.image.load("images/bg2.jpg").convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    register_surface = TITLE_FONT.render("REGISTER", True, PCBUTTON)  # Color blanco (#FFFFFF)
    register_rect = register_surface.get_rect(center=(WIDTH // 2, 50))  # Ajusta las coordenadas según la posición que desees
    special_symbols = ['!', '@', '#', '$', '%', '&', '*', '+', '-', '=', '_', '?', '<', '>', '.', ',', ':', ';']
    
    def  countMusic(username):
        data_encript= Usuario.encripta(username)
        id=Usuario.getID(data_encript)
        lista_song=Musica.getMusic(id)
        nameArtis=Musica.NameArtist(id)
        list_input_song=[]
        number=len(nameArtis[0])
        print(nameArtis)
        for i in range(3):
            print(i)
            if number==i:
                list_input_song.append('')
            else:
                list_input_song.append(nameArtis[0][i])
        return list_input_song

        """for i in range(number):
            list_title_song=TITLE_DATA.render(f"song {i}", True, PCBUTTON)  # Color blanco (#FFFFFF)
            lista_input_song.append(TextInputBox(WIDTH/3, HEIGHT/14.4*9+20*i, WIDTH/7*2, 40, PCBUTTON,SCBUTTON,f'song:{nameArtis[0][i]}'))
        return lista_input_song,list_title_song"""

    running = True
    email_surface = TITLE_DATA.render("Email", True, PCBUTTON)  # Color blanco (#FFFFFF)
    name_surface = TITLE_DATA.render("name", True, PCBUTTON)  # Color blanco (#FFFFFF)
    username_surface = TITLE_DATA.render("username", True, PCBUTTON)  # Color blanco (#FFFFFF)
    age_surface = TITLE_DATA.render("age", True, PCBUTTON)  # Color blanco (#FFFFFF)
    password_surface = TITLE_DATA.render("password", True, PCBUTTON)  # Color blanco (#FFFFFF)
    confirmPassword_surface = TITLE_DATA.render("confirm password", True, PCBUTTON)  # Color blanco (#FFFFFF)
    song1_surface = TITLE_DATA.render("song1", True, PCBUTTON)  # Color blanco (#FFFFFF)
    song2_surface = TITLE_DATA.render("song2", True, PCBUTTON)  # Color blanco (#FFFFFF)
    song3_surface = TITLE_DATA.render("song3", True, PCBUTTON)  # Color blanco (#FFFFFF)


    email_rect = email_surface.get_rect(center=(WIDTH/3-80, HEIGHT/14.4*3+20))  # Ajusta las coordenadas según la posición que 
    name_rect = name_surface.get_rect(center=(WIDTH/3-80, HEIGHT/14.4*4+20))  # Ajusta las coordenadas según la posición que desees
    username_rect = username_surface.get_rect(center=(WIDTH/3-80, HEIGHT/14.4*5+20))  # Ajusta las coordenadas según la posición que desees
    age_rect = age_surface.get_rect(center=(WIDTH/3-80, HEIGHT/14.4*6+20))  # Ajusta las coordenadas según la posición que desees
    password_rect = password_surface.get_rect(center=(WIDTH/3-80, HEIGHT/14.4*7+20))  # Ajusta las coordenadas según la posición que desees
    confirmPassword_rect = confirmPassword_surface.get_rect(center=(WIDTH/3-80, HEIGHT/14.4*8+20))  # Ajusta las coordenadas según la posición que desees
    song1_rect = song1_surface.get_rect(center=(WIDTH/3-80, HEIGHT/14.4*9+20))  # Ajusta las coordenadas según la posición que desees
    song2_rect = song2_surface.get_rect(center=(WIDTH/3-80, HEIGHT/14.4*10+20))  # Ajusta las coordenadas según la posición que desees
    song3_rect = song3_surface.get_rect(center=(WIDTH/3-80, HEIGHT/14.4*11+20))  # Ajusta las coordenadas según la posición que desees
  
   
   
    song_input=countMusic('daniel17')
    print(f'llamada a la base de datos {song_input}')
    email_input = TextInputBox(WIDTH/3, HEIGHT/14.4*3, WIDTH/7*2, 40,PCBUTTON,SCBUTTON, "Email")
    name_input = TextInputBox(WIDTH/3, HEIGHT/14.4*4, WIDTH/7*2, 40,PCBUTTON,SCBUTTON, "Name")
    age_input = TextInputBox(WIDTH/3, HEIGHT/14.4*5, WIDTH/7*2, 40,PCBUTTON,SCBUTTON, "Age")
    username_input = TextInputBox(WIDTH/3, HEIGHT/14.4*6, WIDTH/7*2, 40,PCBUTTON,SCBUTTON, "Username")
    password_input = TextInputBox(WIDTH/3, HEIGHT/14.4*7, WIDTH/7*2, 40,PCBUTTON,SCBUTTON, "Password",is_password=True)
    confirm_password_input = TextInputBox(WIDTH/3, HEIGHT/14.4*8, WIDTH/7*2, 40, PCBUTTON,SCBUTTON,"Confirm Password",is_password=True)
    song1_input=TextInputBox(WIDTH/3, HEIGHT/14.4*9+20, WIDTH/7*2, 40, PCBUTTON,SCBUTTON,f'song:{song_input[0]}')
    song2_input=TextInputBox(WIDTH/3, HEIGHT/14.4*10+20, WIDTH/7*2, 40, PCBUTTON,SCBUTTON,f'song:{song_input[1]}')
    song3_input=TextInputBox(WIDTH/3, HEIGHT/14.4*11+20, WIDTH/7*2, 40, PCBUTTON,SCBUTTON,f'song:{song_input[2]}')
    
    

    

    font = pygame.font.Font(None, 30)
   
   
    while running:
        win.fill(BACKGROUND)
        time_delta = pygame.time.Clock().tick(60)/1000.0
        for event in pygame.event.get():
            email_input.handle_event(event,PCBUTTON,SCBUTTON)
            age_input.handle_event(event,PCBUTTON,SCBUTTON)
            username_input.handle_event(event,PCBUTTON,SCBUTTON)
            password_input.handle_event(event,PCBUTTON,SCBUTTON)
            confirm_password_input.handle_event(event,PCBUTTON,SCBUTTON)
            song1_input.handle_event(event,PCBUTTON,SCBUTTON)
            song2_input.handle_event(event,PCBUTTON,SCBUTTON)
            song3_input.handle_event(event,PCBUTTON,SCBUTTON)
           
           
            manager.process_events(event)
            
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
    
        email_input.update()
        age_input.update()
        username_input.update()
        password_input.update()
        confirm_password_input.update()
        name_input.update()
        song1_input.update()
        song2_input.update()
        song3_input.update()

        register_surface = TITLE_FONT.render("EDID YOUR INFORMATION", True, PCBUTTON)

        win.blit(register_surface, register_rect)
        win.blit(email_surface, email_rect)
        win.blit(name_surface, name_rect)
        win.blit(age_surface, age_rect)
        win.blit(username_surface, username_rect)
        
        win.blit(password_surface, password_rect)
        win.blit(confirmPassword_surface,confirmPassword_rect)
        win.blit(song1_surface, song1_rect)
        win.blit(song2_surface, song2_rect)
        win.blit(song3_surface, song3_rect)

        email_input.draw(win)
        age_input.draw(win)
        username_input.draw(win)
        password_input.draw(win)
        confirm_password_input.draw(win)
        name_input.draw(win)
        song1_input.draw(win)
        song2_input.draw(win)
        song3_input.draw(win)
       
            

        # Actualizar pygame_gui
        manager.update(time_delta)
        manager.draw_ui(win)
        pygame.display.flip()
    pygame.quit()
    sys.exit()

        
         
editScreen()
