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
from edit import edit,editsong
from validate import validate_age,validate_password,validate_email,validate_username
#from ImgRedon import cargar_imagen_redondeada


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
    FONTEdit = pygame.font.Font("font/DejaVuSans.ttf", 20)

# Configuración de la pantalla
    WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
    # Configurar el rectángulo para la vista previa de la cámara
    camera_preview_rect = pygame.Rect(WIDTH/7*4, HEIGHT/14.4*3, WIDTH/7*2-55, HEIGHT/14.4*4)

    #camera_image = None  # Inicializar la imagen de la cámara fuera del bucle princUIDal
    #initial_image_surface = pygame.transform.scale(image_pp, (camera_preview_rect.width, camera_preview_rect.height))

    iconEsc=pygame.image.load("./images/game/escIcon.png")
    iconEsc=pygame.transform.scale(iconEsc, (50,50))
    iconEscRect=iconEsc.get_rect()
    iconEscRect.topleft=(WIDTH//2+100,HEIGHT//5-10)
    
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
    def musicUpdate(username):
        id= Usuario.getID(username)
        nameArtis=Musica.NameArtist(id)
        list_input_song=[]
        number=len(nameArtis)
        print(number)
        for i in range(4):
            if i==3:
                return list_input_song
            elif number-1<i:
                list_input_song.append(('',""))
            
            else:
                list_input_song.append(nameArtis[i]) 

    music=musicUpdate(username)       

    def  countMusic(username):
        id= Usuario.getID(username)
        nameArtis=Musica.NameArtist(id)
        list_input_song=[]
        number=len(nameArtis)
        print('musica',nameArtis,number)
        for i in range(4):
        
        
            if i==3:
                print(i)
                return list_input_song
            elif number-1<i:
                print("elif",i)
                list_input_song.append('')
                #list_input_song.append(f'{ nameArtis[i][0] } by {nameArtis[i][1]}')
            
            else:
                print("else",i)
                list_input_song.append(f'{ nameArtis[i][0] } by {nameArtis[i][1]}')
        
    

        """for i in range(number):
            list_title_song=TITLE_DATA.render(f"song {i}", True, PCBUTTON)  # Color blanco (#FFFFFF)
            lista_input_song.append(TextInputBox(WIDTH/3, HEIGHT/14.4*9+20*i, WIDTH/7*2, 40, PCBUTTON,SCBUTTON,f'song:{nameArtis[0][i]}'))
        return lista_input_song,list_title_song"""
    song_input=countMusic(username)
    print("songs count",song_input)
    id=Usuario.getID(username)
    email=Usuario.getEmail(id)
    name=Usuario.getName(id)
    age=Usuario.getAge(id)
    username=Usuario.getUsername(id)
    running = True
    email_surface = FONTEdit.render(f"Email: {email}", True, PCBUTTON)  # Color blanco (#FFFFFF)
    name_surface = FONTEdit.render(f"name: {name}", True, PCBUTTON)  # Color blanco (#FFFFFF)
    username_surface = FONTEdit.render(f"username: {username}", True, PCBUTTON)  # Color blanco (#FFFFFF)
    age_surface = FONTEdit.render(f"age: {age}", True, PCBUTTON)  # Color blanco (#FFFFFF)
    password_surface = FONTEdit.render(f"password", True, PCBUTTON)  # Color blanco (#FFFFFF)
    confirmPassword_surface = FONTEdit.render("confirm password", True, PCBUTTON)  # Color blanco (#FFFFFF)
    song1_surface = FONTEdit.render(f"song1: {song_input[0]}", True, PCBUTTON)  # Color blanco (#FFFFFF)
    song2_surface = FONTEdit.render(f"song2: {song_input[1]}", True, PCBUTTON)  # Color blanco (#FFFFFF)
    song3_surface = FONTEdit.render(f"song3: {song_input[2]}", True, PCBUTTON) # Color blanco (#FFFFFF)


    email_rect = email_surface.get_rect()  # Ajusta las coordenadas según la posición que 
    email_rect.topleft=(WIDTH/3-200, HEIGHT/14.4*3+80)

    name_rect = name_surface.get_rect()  # Ajusta las coordenadas según la posición que desees
    name_rect.topleft=(WIDTH/3-200, HEIGHT/14.4*3+120)
    username_rect = username_surface.get_rect()  # Ajusta las coordenadas según la posición que desees
    username_rect.topleft=(WIDTH/3-200, HEIGHT/14.4*3+160)
    age_rect = age_surface.get_rect()  # Ajusta las coordenadas según la posición que desees
    age_rect.topleft=(WIDTH/3-200, HEIGHT/14.4*3+200)
    
    password_rect = password_surface.get_rect()  # Ajusta las coordenadas según la posición que desees
    password_rect.topleft=(WIDTH/3-200, HEIGHT/14.4*3+240)
    confirmPassword_rect = confirmPassword_surface.get_rect()  # Ajusta las coordenadas según la posición que desees
    confirmPassword_rect.topleft=(WIDTH/3-200, HEIGHT/14.4*3+280)
    song1_rect = song1_surface.get_rect()  # Ajusta las coordenadas según la posición que desees
    song1_rect.topleft=(WIDTH/3-200, HEIGHT/14.4*3+320)
    
    song2_rect = song2_surface.get_rect()  # Ajusta las coordenadas según la posición que desees
    song2_rect.topleft=(WIDTH/3-200, HEIGHT/14.4*3+360)
    
    song3_rect = song3_surface.get_rect()  # Ajusta las coordenadas según la posición que desees
    song3_rect.topleft=(WIDTH/3-200, HEIGHT/14.4*3+400)
    
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
    
    buton_email=Button('Editar',80,30,(WIDTH/3+200,HEIGHT/14.4*3+80),5,SCBUTTON,FONTEdit)
    buton_name=Button('Editar',80,30,(WIDTH/3+200,HEIGHT/14.4*3+120),5,SCBUTTON,FONTEdit)
    buton_age=Button('Editar',80,30,(WIDTH/3+200,HEIGHT/14.4*3+200),5,SCBUTTON,FONTEdit)
    buton_username=Button('Editar',80,30,(WIDTH/3+200,HEIGHT/14.4*3+160),5,SCBUTTON,FONTEdit)
    buton_password=Button('Editar',80,30,(WIDTH/3+200,HEIGHT/14.4*3+240),5,SCBUTTON,FONTEdit)
    buton_confirmpassword=Button('Editar',80,30,(WIDTH/3+200,HEIGHT/14.4*3+280),5,SCBUTTON,FONTEdit)
    buton_song1=Button('Editar',80,30,(WIDTH/3+200,HEIGHT/14.4*3+320),5,SCBUTTON,FONTEdit)
    buton_song2=Button('Editar',80,30,(WIDTH/3+200,HEIGHT/14.4*3+360),5,SCBUTTON,FONTEdit)
    buton_song3=Button('Editar',80,30,(WIDTH/3+200,HEIGHT/14.4*3+400),5,SCBUTTON,FONTEdit)
    buton_photo=Button('Editar',80,30,(WIDTH/3+650,HEIGHT/14.4*3+350),5,SCBUTTON,FONTEdit)

    font = pygame.font.Font(None, 30)
   

    selected_image_surface = load_selected_image(f'./profile_photos/{Usuario.getID(username)}.png')  # Establecer la imagen inicial
    def add_frame(image_surface, frame_width, frame_color):
        framed_surface = pygame.Surface((image_surface.get_width() + 2 * frame_width, image_surface.get_height() + 2 * frame_width), pygame.SRCALPHA)
        pygame.draw.rect(framed_surface, frame_color, (0, 0, framed_surface.get_width(), framed_surface.get_height()), frame_width)
        framed_surface.blit(image_surface, (frame_width, frame_width))
        return framed_surface
##
    
    #selected_image_surface=cargar_imagen_redondeada(selected_image_surface,500,500)
    #profile_surface.blit(selected_image_surface, (0, 0))
    #ventana_correo = screenEmer(400, 400, win)
    #lienzo_correo = ventana_correo.surfaceEmer()
    while running:
        win.fill(BACKGROUND)
        crear_rectangulo_redondeado(hex_to_rgb(SCBUTTON),WIDTH/7+10, HEIGHT/14.4*3-20, WIDTH/7*3+50, HEIGHT/14.4*8+100,15,alpha=200,win=win)
        crear_rectangulo_redondeado(hex_to_rgb(TCBUTTOM),WIDTH/7+30, HEIGHT/14.4*3+50, WIDTH/7*3, HEIGHT/14.4*8,15,alpha=200,win=win)
        crear_rectangulo_redondeado(hex_to_rgb(PCBUTTON),WIDTH/7+700, HEIGHT/14.4*3+20, WIDTH/7*2+100, HEIGHT/14.4*8,15,alpha=200,win=win)
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
                    print("email")
                    edit(id,editScreen,username,WIDTH,HEIGHT,Usuario.updateEmail,"EDITAR EMAIL","This email is already taken. Please choose another one.",validate_email,'Email','Please enter a valid email address')
                elif buton_name.top_rect.collidepoint(mouse_pos):
                    print("name") 
                    edit(id,editScreen,username,WIDTH,HEIGHT,Usuario.updateName,"EDITAR Name","",None,'Name',"")
                elif buton_age.top_rect.collidepoint(mouse_pos):
                    edit(id,editScreen,username,WIDTH,HEIGHT,Usuario.updateAge,"EDITAR Age","",validate_age,'Age',"Password must be at least 8 characters long with at least one uppercase letter and one special symbol")
                elif buton_username.top_rect.collidepoint(mouse_pos):
                    edit(id,editScreen,username,WIDTH,HEIGHT,Usuario.updateUsername,"EDITAR Username","This username is already taken. Please choose another one",validate_username,'Username','Username contains prohibited words')
                elif buton_song1.top_rect.collidepoint(mouse_pos):
                    editsong(id,editScreen,username,WIDTH,HEIGHT,Musica.upadateSong,music[0][0],music[0][1],"EDITAR cancion")
                elif buton_song2.top_rect.collidepoint(mouse_pos):
                    editsong(id,editScreen,username,WIDTH,HEIGHT,Musica.upadateSong,music[1][0],music[1][1],"EDITAR cancion")
                elif buton_song3.top_rect.collidepoint(mouse_pos):
                    editsong(id,editScreen,username,WIDTH,HEIGHT,Musica.upadateSong,music[2][0],music[2][1],"EDITAR cancion")
                elif buton_photo.top_rect.collidepoint(mouse_pos):
                   pass
    
                elif iconEscRect.collidepoint(mouse_pos):
                    print('icon')
                    running=False

                    sys.exit()      
                  
       
        #selected_image_surface=(hex_to_rgb(BACKGROUND),(WIDTH//60*25), 7, ((WIDTH//60)*11), (80),15,alpha=95,win=win)
        
        #cargar_imagen_redondeada(selected_image_surface,win,100,100,selected_image_surface.get_width(),selected_image_surface.get_height())
   
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
        win.blit(iconEsc,iconEscRect)
        #win.blit(lienzo_correo, (100, 200))
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
       
        # Actualizar pygame_gui"""
        manager.update(time_delta)
        manager.draw_ui(win)
        buton_email.draw(PCBUTTON,TCBUTTOM,win)
        buton_name.draw(PCBUTTON,TCBUTTOM,win)
        buton_username.draw(PCBUTTON,TCBUTTOM,win)
        buton_age.draw(PCBUTTON,TCBUTTOM,win)
        buton_password.draw(PCBUTTON,TCBUTTOM,win)
        buton_confirmpassword.draw(PCBUTTON,TCBUTTOM,win)
        buton_song1.draw(PCBUTTON,TCBUTTOM,win)
        buton_song2.draw(PCBUTTON,TCBUTTOM,win)
        buton_song3.draw(PCBUTTON,TCBUTTOM,win)
        buton_photo.draw(SCBUTTON,TCBUTTOM,win)
        framed_image = add_frame(selected_image_surface, 10, (255, 255, 255))
        #win.blit(selected_image_surface, (camera_preview_rect.x+200, camera_preview_rect.y)) 
        win.blit(framed_image, (camera_preview_rect.x+220, camera_preview_rect.y+110)) 
        pygame.display.flip()
    pygame.quit()
    sys.exit()

        
         
editScreen('daniel')
