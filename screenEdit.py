import pygame
import pygame_gui
from TextInputBox import TextInputBox
import sys
from objectbasedata import Usuario, Musica
from Button import Button
import validate
import sys
import os
from emergeScreen import screenEmer
from rect_redon import crear_rectangulo_redondeado
from ImgRedon import cargar_imagen_redondeada

def editScreen(username):
    pygame.init()
    screen_info = pygame.display.Info()

    BACKGROUND = '#005b4d'
    PCBUTTON = '#01F0BF'
    SCBUTTON = '#00A383'
    TCBUTTOM = '#006350'
    TITLE_FONT = pygame.font.Font("font/KarmaFuture.ttf", 50)
    FONT = pygame.font.Font("font/DejaVuSans.ttf", 20)
    FONT_SEC = pygame.font.Font("font/DejaVuSans.ttf", 20)
    FONTEdit = pygame.font.Font("font/DejaVuSans.ttf", 10)

# Configuración de la pantalla
    WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
    # Configurar el rectángulo para la vista previa de la cámara
    camera_preview_rect = pygame.Rect(WIDTH/7*4, HEIGHT/14.4*3, WIDTH/7*2-55, HEIGHT/14.4*4)

    #camera_image = None  # Inicializar la imagen de la cámara fuera del bucle princUIDal
    #initial_image_surface = pygame.transform.scale(image_pp, (camera_preview_rect.width, camera_preview_rect.height))


    profile_surface = pygame.Surface((camera_preview_rect.width, camera_preview_rect.height))
    profile_surface.fill(SCBUTTON)


    def load_selected_image(image_path):
        if os.path.exists(image_path):
            image_surface = pygame.image.load(image_path).convert()
            return pygame.transform.scale(image_surface, (camera_preview_rect.width, camera_preview_rect.height))
        return None
    
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


    win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Eagle Defender")

    manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    selected_image_surface = None
    camera_on = False
    UID_device = None
    FONT = pygame.font.Font("font/KarmaFuture.ttf", 20)
    TITLE_FONT = pygame.font.Font(None,60)
    TITLE_DATA = pygame.font.Font(None,20)
    FONT_SEC =pygame.font.Font("font/KarmaFuture.ttf", 20)
    background_image = pygame.image.load("images/bg2.jpg").convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    register_surface = TITLE_FONT.render("REGISTER", True, PCBUTTON)  # Color blanco (#FFFFFF)
    register_rect = register_surface.get_rect(center=(WIDTH // 2, 50))  # Ajusta las coordenadas según la posición que desees
    special_symbols = ['!', '@', '#', '$', '%', '&', '*', '+', '-', '=', '_', '?', '<', '>', '.', ',', ':', ';']
    
    def  countMusic(username):
        id= Usuario.getID(username)
        nameArtis=Musica.NameArtist(id)
        list_input_song=[]
        number=len(nameArtis[0])
        print(nameArtis)
        for i in range(3):
            print(i)
            if number==i:
                list_input_song.append('')
                return list_input_song
            else:
                list_input_song.append(f'{ nameArtis[i][0] } by {nameArtis[i][1]}')
        
    

        """for i in range(number):
            list_title_song=TITLE_DATA.render(f"song {i}", True, PCBUTTON)  # Color blanco (#FFFFFF)
            lista_input_song.append(TextInputBox(WIDTH/3, HEIGHT/14.4*9+20*i, WIDTH/7*2, 40, PCBUTTON,SCBUTTON,f'song:{nameArtis[0][i]}'))
        return lista_input_song,list_title_song"""
    song_input=countMusic(username)
    print(f'llamada a la base de datos {song_input}')
    id=Usuario.getID(username)
    email=Usuario.getEmail(id)
    name=Usuario.getName(id)
    age=Usuario.getAge(id)
    username=Usuario.getUsername(id)
    running = True
    email_surface = TITLE_DATA.render(f"Email: {email}", True, PCBUTTON)  # Color blanco (#FFFFFF)
    name_surface = TITLE_DATA.render(f"name: {name}", True, PCBUTTON)  # Color blanco (#FFFFFF)
    username_surface = TITLE_DATA.render(f"username: {username}", True, PCBUTTON)  # Color blanco (#FFFFFF)
    age_surface = TITLE_DATA.render(f"age: {age}", True, PCBUTTON)  # Color blanco (#FFFFFF)
    password_surface = TITLE_DATA.render(f"password", True, PCBUTTON)  # Color blanco (#FFFFFF)
    confirmPassword_surface = TITLE_DATA.render("confirm password", True, PCBUTTON)  # Color blanco (#FFFFFF)
    song1_surface = TITLE_DATA.render(f"song1: {song_input[0]}", True, PCBUTTON)  # Color blanco (#FFFFFF)
    song2_surface = TITLE_DATA.render(f"song2: {song_input[1]}", True, PCBUTTON)  # Color blanco (#FFFFFF)
    song3_surface = TITLE_DATA.render(f"song3: {song_input[2]}", True, PCBUTTON) # Color blanco (#FFFFFF)


    email_rect = email_surface.get_rect()  # Ajusta las coordenadas según la posición que 
    email_rect.topleft=(WIDTH/3-80, HEIGHT/14.4*3+80)

    name_rect = name_surface.get_rect()  # Ajusta las coordenadas según la posición que desees
    name_rect.topleft=(WIDTH/3-80, HEIGHT/14.4*3+120)
    username_rect = username_surface.get_rect()  # Ajusta las coordenadas según la posición que desees
    username_rect.topleft=(WIDTH/3-80, HEIGHT/14.4*3+160)
    age_rect = age_surface.get_rect()  # Ajusta las coordenadas según la posición que desees
    age_rect.topleft=(WIDTH/3-80, HEIGHT/14.4*3+200)
    
    password_rect = password_surface.get_rect()  # Ajusta las coordenadas según la posición que desees
    password_rect.topleft=(WIDTH/3-80, HEIGHT/14.4*3+240)
    confirmPassword_rect = confirmPassword_surface.get_rect()  # Ajusta las coordenadas según la posición que desees
    confirmPassword_rect.topleft=(WIDTH/3-80, HEIGHT/14.4*3+280)
    song1_rect = song1_surface.get_rect()  # Ajusta las coordenadas según la posición que desees
    song1_rect.topleft=(WIDTH/3-80, HEIGHT/14.4*3+320)
    
    song2_rect = song2_surface.get_rect()  # Ajusta las coordenadas según la posición que desees
    song2_rect.topleft=(WIDTH/3-80, HEIGHT/14.4*3+360)
    
    song3_rect = song3_surface.get_rect()  # Ajusta las coordenadas según la posición que desees
    song3_rect.topleft=(WIDTH/3-80, HEIGHT/14.4*3+400)
    
    email_input = TextInputBox(WIDTH/3, HEIGHT/14.4*3, WIDTH/7*2, 40,PCBUTTON,SCBUTTON, f"{email}")
    name_input = TextInputBox(WIDTH/3, HEIGHT/14.4*4, WIDTH/7*2, 40,PCBUTTON,SCBUTTON, f"Name {name}")
    age_input = TextInputBox(WIDTH/3, HEIGHT/14.4*5, WIDTH/7*2, 40,PCBUTTON,SCBUTTON,f"Age{age}")
    username_input = TextInputBox(WIDTH/3, HEIGHT/14.4*6, WIDTH/7*2, 40,PCBUTTON,SCBUTTON, f"Username {username}")
    password_input = TextInputBox(WIDTH/3, HEIGHT/14.4*7, WIDTH/7*2, 40,PCBUTTON,SCBUTTON, f"Password",is_password=True)
    confirm_password_input = TextInputBox(WIDTH/3, HEIGHT/14.4*8, WIDTH/7*2, 40, PCBUTTON,SCBUTTON,"Confirm Password",is_password=True)
    song1_input=TextInputBox(WIDTH/3, HEIGHT/14.4*9+20, WIDTH/7*2, 40, PCBUTTON,SCBUTTON,f'song:{song_input[0]}')
    song2_input=TextInputBox(WIDTH/3, HEIGHT/14.4*10+20, WIDTH/7*2, 40, PCBUTTON,SCBUTTON,f'song:{song_input[1]}')
    song3_input=TextInputBox(WIDTH/3, HEIGHT/14.4*11+20, WIDTH/7*2, 40, PCBUTTON,SCBUTTON,f'song:{song_input[2]}')
    #Edit_button = Button('Edit info',400,40,(WIDTH/3,HEIGHT/7*2+450),5,SCBUTTON)
    
    buton_email=Button('Editar',50,20,(WIDTH/3+150,HEIGHT/14.4*3+80),5,SCBUTTON,FONTEdit)
    buton_name=Button('Editar',50,20,(WIDTH/3+150,HEIGHT/14.4*3+120),5,SCBUTTON,FONTEdit)
    buton_age=Button('Editar',50,20,(WIDTH/3+150,HEIGHT/14.4*3+160),5,SCBUTTON,FONTEdit)
    buton_username=Button('Editar',50,20,(WIDTH/3+150,HEIGHT/14.4*3+200),5,SCBUTTON,FONTEdit)
    buton_password=Button('Editar',50,20,(WIDTH/3+150,HEIGHT/14.4*3+240),5,SCBUTTON,FONTEdit)
    buton_confirmpassword=Button('Editar',50,20,(WIDTH/3+150,HEIGHT/14.4*3+280),5,SCBUTTON,FONTEdit)
    buton_song1=Button('Editar',50,20,(WIDTH/3+150,HEIGHT/14.4*3+320),5,SCBUTTON,FONTEdit)
    buton_song2=Button('Editar',50,20,(WIDTH/3+150,HEIGHT/14.4*3+360),5,SCBUTTON,FONTEdit)
    buton_song3=Button('Editar',50,20,(WIDTH/3+150,HEIGHT/14.4*3+400),5,SCBUTTON,FONTEdit)

    def updateEmail(id):
        wind=screenEmer(400,400,win)
        canvas=wind.show()
        email_input.draw(canvas)
        

        #Usuario.updateEmail(id,email)
    def updateName(id):
        Usuario.updateName(id,name)
    def updatePassword(id):
        #Usuario.updatePassword(id,password)
        pass
    def updateUsername(id):
        Usuario.updateUsername(id,username)
    def updateAge(id):
        Age=15
        Usuario.updateAge(id,Age)
    def updateSong1(id,Age):
        pass
        #Musica.updateEmail(id,email)
    def updateSong2(id,song2):
        pass
        #Musica.updateSong2(id,song2)
    def updateSong3(id,song3):
        pass
        #Musica.updateSong3(id,song3)

    font = pygame.font.Font(None, 30)
   

    selected_image_surface = load_selected_image(f'./profile_photos/{Usuario.getID(username)}.png')  # Establecer la imagen inicial
    
##
    
    #selected_image_surface=cargar_imagen_redondeada(selected_image_surface,500,500)
    #profile_surface.blit(selected_image_surface, (0, 0))
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
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if buton_email.top_rect.collidepoint(mouse_pos):
                    updateEmail(id)
                elif buton_name.top_rect.collidepoint(mouse_pos):
                    updateName(id)
                elif buton_username.top_rect.collidepoint(mouse_pos):
                    updateUsername(id)
                elif buton_password.top_rect.collidepoint(mouse_pos):
                    updatePassword(id)
                elif buton_age.top_rect.collidepoint(mouse_pos):
                    updateAge(id)
                if buton_email.top_rect.collidepoint(mouse_pos):
                    updateEmail()
                
        crear_rectangulo_redondeado(hex_to_rgb(SCBUTTON),WIDTH/7-10, HEIGHT/14.4*3-10, WIDTH/7*3+50, HEIGHT/14.4*8,15,alpha=200,win=win)
        crear_rectangulo_redondeado(hex_to_rgb(TCBUTTOM),WIDTH/7+30, HEIGHT/14.4*3+50, WIDTH/7*3, HEIGHT/14.4*8,15,alpha=200,win=win)
        #(hex_to_rgb(BACKGROUND),(WIDTH//60*25), 7, ((WIDTH//60)*11), (80),15,alpha=95,win=win)
        
        cargar_imagen_redondeada(selected_image_surface,win,100,100,selected_image_surface.get_width(),selected_image_surface.get_height())
   
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
        """
        email_input.draw(win)
        age_input.draw(win)
        username_input.draw(win)
        password_input.draw(win)
        confirm_password_input.draw(win)
        name_input.draw(win)
        song1_input.draw(win)
        song2_input.draw(win)
        song3_input.draw(win)
        Edit_button.draw(PCBUTTON,TCBUTTOM,win)
        win.blit(selected_image_surface, (camera_preview_rect.x+200, camera_preview_rect.y)) 
       
        # Actualizar pygame_gui
        manager.update(time_delta)
        manager.draw_ui(win)"""
        buton_email.draw(PCBUTTON,TCBUTTOM,win)
        buton_name.draw(PCBUTTON,TCBUTTOM,win)
        buton_username.draw(PCBUTTON,TCBUTTOM,win)
        buton_age.draw(PCBUTTON,TCBUTTOM,win)
        buton_password.draw(PCBUTTON,TCBUTTOM,win)
        buton_confirmpassword.draw(PCBUTTON,TCBUTTOM,win)
        buton_song1.draw(PCBUTTON,TCBUTTOM,win)
        buton_song2.draw(PCBUTTON,TCBUTTOM,win)
        buton_song3.draw(PCBUTTON,TCBUTTOM,win)
       #win.blit(selected_image_surface, (camera_preview_rect.x+200, camera_preview_rect.y)) 
        pygame.display.flip()
    pygame.quit()
    sys.exit()

        
         
editScreen('daniel')
