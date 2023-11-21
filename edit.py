import pygame
from TextInputBox import TextInputBox
from objectbasedata import Usuario
from Button import Button
import sys
from chooseMusic import list_music
from showMessage import mostrar_mensaje_error
from objectbasedata import Musica
import pygame_gui
from folder import select_folder
import threading
import os
import pygame.camera

def edit(id,screen,username,width,height,updateFunct,Titulo,mensaje,validateFunct,data,validateError,game,lista):
    pygame.init()
    screen_info = pygame.display.Info()
    FONTEdit = pygame.font.Font("font/DejaVuSans.ttf", 30)
    BACKGROUND = '#005b4d'
    PCBUTTON = '#01F0BF'
    SCBUTTON = '#00A383'
    TCBUTTOM = '#006350'
    FONT = pygame.font.Font("font/DejaVuSans.ttf", 40)

    window = pygame.display.set_mode((width,height))
    pygame.display.set_caption(f"{Titulo}")

    input = TextInputBox(width//2-150, height//2-40, 300, 40, PCBUTTON, SCBUTTON, "Enter new email")
    iconEsc=pygame.image.load("./images/game/escIcon.png")
    iconEsc=pygame.transform.scale(iconEsc, (50,50))
    iconEscRect=iconEsc.get_rect()
    iconEscRect.topleft=(width//2+300,height//5-10)
    

    buton_email=Button('Editar',100,40,(width/3+400,height//2-40),5,SCBUTTON,FONTEdit)
    running = True
    while running:
        window.fill(BACKGROUND)
        for event in pygame.event.get():
            input.handle_event(event, PCBUTTON, SCBUTTON)
            if event.type == pygame.QUIT:
                running = False
                screen(username,width,height,game,lista)
                

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if buton_email.top_rect.collidepoint(mouse_pos):
                    newValue = input.get_text()
                    #Usuario.updateEmail(id,new_email)
                    if validateFunct==None:
                        response=updateFunct(id,newValue)
                        if response==-1:
                            mostrar_mensaje_error(f"Usuario {username}",mensaje , PCBUTTON, SCBUTTON,window,width,height)
                    elif not validateFunct(newValue):
                        mostrar_mensaje_error(f'Invalid {data}',validateError,PCBUTTON,SCBUTTON,window,width,height)
                        
                    else:
                        response=updateFunct(id,newValue)
                        if response==-1:
                            mostrar_mensaje_error(f"Usuario {username}",mensaje , PCBUTTON, SCBUTTON,window,width,height)

                elif iconEscRect.collidepoint(mouse_pos):
                    running=False
                    screen(username,width,height,game,lista)
                    


        input.update()
        input.draw(window)
        buton_email.draw(PCBUTTON,TCBUTTOM,window)
        window.blit(iconEsc,iconEscRect)
        pygame.display.flip()

    
    #Usuario.updateEmail(id, new_email)  # Update the email in the database
    pygame.quit()




def editsong(id,screen,username,width,height,updateFunct,name,artist,Titulo,game,lista):
    pygame.init()
    screen_info = pygame.display.Info()
    FONTEdit = pygame.font.Font("font/DejaVuSans.ttf", 30)
    BACKGROUND = '#005b4d'
    PCBUTTON = '#01F0BF'
    SCBUTTON = '#00A383'
    TCBUTTOM = '#006350'
    FONT = pygame.font.Font("font/DejaVuSans.ttf", 20)
    font = pygame.font.Font(None, 30)
    text_color = (255, 255, 255)

   
    window = pygame.display.set_mode((width,height))
    pygame.display.set_caption(f"{Titulo}")

    input = TextInputBox(width//2-5, height//2-40, 300, 40, PCBUTTON, SCBUTTON, "Enter music")
    iconEsc=pygame.image.load("./images/game/escIcon.png")
    iconEsc=pygame.transform.scale(iconEsc, (50,50))
    iconEscRect=iconEsc.get_rect()
    iconEscRect.topleft=(width//2+300,height//5-10)
    surfaceMusic=pygame.Surface((width/6+20,40))
    search_music_button=Button('buscar cancion',250,60,(width//2+350, height//2-40),5,SCBUTTON,FONTEdit)
    add_music_button=Button('Editar',100,30,(width//2+350, height//2+40),5,SCBUTTON,FONTEdit)
    running = True
    set_music=[]
    scroll_offset = 0  # Desplazamiento de la lista de canciones
    song_display_limit = 1  # Número de canciones visibles a la vez
    
    while running:
        window.fill(BACKGROUND)
        for event in pygame.event.get():
            input.handle_event(event, PCBUTTON, SCBUTTON)
            if event.type == pygame.QUIT:
                running = False
                screen(username,width,height,game,lista)
            
            #eventos de la musica
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if scroll_offset > 0:
                        scroll_offset -= 1
                elif event.key == pygame.K_DOWN:
                    if scroll_offset < len(set_music) - song_display_limit:
                        scroll_offset += 1

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if search_music_button.top_rect.collidepoint(mouse_pos):
                    newValue = input.get_text()
                    try:
                        set_music=list_music(newValue)
                    #Usuario.updateEmail(id,new_email)
                    except:
                        mostrar_mensaje_error("Canciones Favoritas", 'Escribe la canción para poder mostrarte los resultados' , PCBUTTON, SCBUTTON,window,width,height)

                elif add_music_button.top_rect.collidepoint(event.pos):
                    music=set_music[i]
                    newName=music["name_song"]
                    
                    newArtist=music['name_artist']
                    
                    newUrl=music['url']
                    print(newName,newArtist,newUrl)
                    if name=="" and artist=="":
                        print("vacio")
                        if Musica.count_song_user(id)==3:
                            print("ya tienes el limite en las canciones")
                        else:
                            newMusic=Musica(id,newName,newArtist,newUrl)
                            newMusic.save_data()
                        
                    else:    
                        print('resultado del update musica',updateFunct(id,newName,newArtist,newUrl,name,artist))

                elif iconEscRect.collidepoint(mouse_pos):
                    running=False
                    screen(username,width,height,game,lista)
                
        surfaceMusic.fill((BACKGROUND ))  # Limpia la pantalla

        y = 20  # Posición vertical inicial para la primera canción a mostrar
        # Dibuja las canciones en la pantalla
        for i in range(scroll_offset, min(scroll_offset + song_display_limit, len(set_music))):

            text = font.render("Artista: " + set_music[i]['name_artist'], True, text_color)
            surfaceMusic.blit(text, (20, 10))
            
        y += 50  # Espaciado entre canciones
        #win.blit(surfaceMusic, (WIDTH/7,HEIGHT/14.4*10))
                    


        input.update()
        input.draw(window)
        search_music_button.draw(PCBUTTON,TCBUTTOM,window)
        window.blit(surfaceMusic, (width//2-5, height//2+40))
        if len(set_music)>0:
               
                add_music_button.draw(PCBUTTON,TCBUTTOM,window)
        window.blit(iconEsc,iconEscRect)
        pygame.display.flip()

    
    #Usuario.updateEmail(id, new_email)  # Update the email in the database
    pygame.quit()




def editImg(id,screen,username,width,height,game,lista):
    pygame.init()
    pygame.camera.init()
    cameras = pygame.camera.list_cameras()

    camera = None
    def load_selected_image(image_path):
        if os.path.exists(image_path):
            image_surface = pygame.image.load(image_path).convert()
            return pygame.transform.scale(image_surface, (camera_preview_rect.width, camera_preview_rect.height))
        return None
    # Itera sobre la lista de cámaras y trata de inicializar cada una
    for cam in cameras:
        try:
            # Intenta inicializar la cámara actual
            camera = pygame.camera.Camera(cam, (width, height))
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
  


    FONTEdit = pygame.font.Font("font/DejaVuSans.ttf", 10)
    manager = pygame_gui.UIManager((width, height))
    selected_image_surface = None
    camera_on = False
    UID_device = None
    FONTEdit = pygame.font.Font("font/DejaVuSans.ttf", 30)
    BACKGROUND = '#005b4d'
    PCBUTTON = '#01F0BF'
    SCBUTTON = '#00A383'
    TCBUTTOM = '#006350'
    FONT = pygame.font.Font("font/DejaVuSans.ttf", 40)

    window = pygame.display.set_mode((width,height))
    camera_preview_rect = pygame.Rect(width/7*4, height/14.4*3, width/7*2-55, height/14.4*4)
    
    iconEsc=pygame.image.load("./images/game/escIcon.png")
    iconEsc=pygame.transform.scale(iconEsc, (50,50))
    iconEscRect=iconEsc.get_rect()
    iconEscRect.topleft=(width//2+300,height//5-10)
    take_foto_button = Button(u'\u25c9',50,40,(width/7*6-50,height/14.4*3+10),5,SCBUTTON,FONTEdit)
    select_image_button = Button(u'\u2191',50,40,(width/7*6-50,height/14.4*4+5),5,SCBUTTON,FONTEdit)
    reset_button = Button(u'\u2716',50,40,(width/7*6-50,height/14.4*6+5),5,SCBUTTON,FONTEdit)
    # Definir un tono de gris con baja transparencia
    PROFILE_COLOR = (200, 200, 200, 50)  # R, G, B, A (A es el canal alfa)

# Crear la superficie con transparencia
    profile_surface = pygame.Surface((camera_preview_rect.width, camera_preview_rect.height), pygame.SRCALPHA)  # Establecer SRCALPHA para el canal alfa
    pygame.draw.rect(profile_surface, PROFILE_COLOR, profile_surface.get_rect())  # Dibujar un rectángulo del color SCBUTTON en la superficie

    
    camera_image = None  
    running = True
    image_pp=pygame.image.load(f'./profile_photos/{Usuario.getID(username)}.png').convert_alpha()  # Establecer la imagen inicial
    initial_image_surface = pygame.transform.scale(image_pp, (camera_preview_rect.width, camera_preview_rect.height))
    selected_image_surface = None
    selected_image_surface = initial_image_surface  # Establecer la imagen inicial
    profile_surface.blit(selected_image_surface, (0, 0))

    while running:
        
        window.fill(BACKGROUND)
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = False
                screen(username,width,height,game,lista)
                

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()



                if select_image_button.top_rect.collidepoint(mouse_pos):
                    if camera:
                        if camera_on:
                            camera.stop()
                            camera_on=False
                    if selected_image_surface==None:
                        initial_image_surface=pygame.transform.scale(image_pp, (camera_preview_rect.width, camera_preview_rect.height))
                        print("imagen inicial")
                                    
                        selected_image_surface= initial_image_surface
                    file_dialog_thread = threading.Thread(target=select_folder)
                    file_dialog_thread.start()
                
                elif take_foto_button.top_rect.collidepoint(mouse_pos):
                    print("camara")
                    if camera:

                        if not camera_on:
                            take_foto_button.update_button('[\u25c9"]',(50,40))
                            selected_image_surface = None
                            camera.start()
                            camera_on=True
                        else:
                            tipo_img =1
                            take_foto_button.update_button('\u25c9',(50,40))
                            if not os.path.exists('profile_photos'):
                                os.makedirs('profile_photos')
                            image = camera.get_image()
                            
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
        
                elif iconEscRect.collidepoint(mouse_pos):
                    running=False
                    screen(username,width,height,game,lista)
                    

        if selected_image_surface:
            if (selected_image_surface==initial_image_surface) :
                window.blit(profile_surface, (camera_preview_rect.x-200, camera_preview_rect.y+20))
            else:
                window.blit(selected_image_surface, (camera_preview_rect.x, camera_preview_rect.y))

        else:
            if camera_on:
                image = camera.get_image()
                camera_image = pygame.transform.scale(image, (camera_preview_rect.width, camera_preview_rect.height))
                window.blit(camera_image, camera_preview_rect.topleft)
        reset_button.draw(PCBUTTON,TCBUTTOM,window)
        select_image_button.draw(PCBUTTON,TCBUTTOM,window)
        take_foto_button.draw(PCBUTTON,TCBUTTOM,window)
       
        window.blit(iconEsc,iconEscRect)
        pygame.display.flip()

    
    #Usuario.updateEmail(id, new_email)  # Update the email in the database
    pygame.quit()