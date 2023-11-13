import pygame
from TextInputBox import TextInputBox
from objectbasedata import Usuario
from Button import Button
import sys
from chooseMusic import list_music
from showMessage import mostrar_mensaje_error
def edit(id,screen,username,width,height,updateFunct,Titulo,mensaje):
    pygame.init()
    screen_info = pygame.display.Info()
    FONTEdit = pygame.font.Font("font/DejaVuSans.ttf", 10)
    BACKGROUND = '#005b4d'
    PCBUTTON = '#01F0BF'
    SCBUTTON = '#00A383'
    TCBUTTOM = '#006350'
    FONT = pygame.font.Font("font/DejaVuSans.ttf", 20)

    WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
    window = pygame.display.set_mode((width,height))
    pygame.display.set_caption(f"{Titulo}")

    input = TextInputBox(width//2-150, height//2-40, 300, 40, PCBUTTON, SCBUTTON, "Enter new email")
    iconEsc=pygame.image.load("./images/game/escIcon.png")
    iconEsc=pygame.transform.scale(iconEsc, (50,50))
    iconEscRect=iconEsc.get_rect()
    iconEscRect.topleft=(WIDTH//2+300,HEIGHT//5-10)
    

    buton_email=Button('Editar',50,20,(WIDTH/3+150,HEIGHT/14.4*3+80),5,SCBUTTON,FONTEdit)
    running = True
    while running:
        window.fill(BACKGROUND)
        for event in pygame.event.get():
            input.handle_event(event, PCBUTTON, SCBUTTON)
            if event.type == pygame.QUIT:
                running = False
                screen(username)
                

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if buton_email.top_rect.collidepoint(mouse_pos):
                    newValue = input.get_text()
                    #Usuario.updateEmail(id,new_email)
                    response=updateFunct(id,newValue)
                    if response==-1:
                        mostrar_mensaje_error(f"Usuario {username}",mensaje , PCBUTTON, SCBUTTON,window,width,height)

                elif iconEscRect.collidepoint(mouse_pos):
                    running=False
                    screen(username)
                    


        input.update()
        input.draw(window)
        buton_email.draw(PCBUTTON,TCBUTTOM,window)
        window.blit(iconEsc,iconEscRect)
        pygame.display.flip()

    
    #Usuario.updateEmail(id, new_email)  # Update the email in the database
    pygame.quit()




def editsong(id,screen,username,width,height,updateFunct,name,artist,Titulo):
    pygame.init()
    screen_info = pygame.display.Info()
    FONTEdit = pygame.font.Font("font/DejaVuSans.ttf", 10)
    BACKGROUND = '#005b4d'
    PCBUTTON = '#01F0BF'
    SCBUTTON = '#00A383'
    TCBUTTOM = '#006350'
    FONT = pygame.font.Font("font/DejaVuSans.ttf", 20)
    font = pygame.font.Font(None, 30)
    text_color = (255, 255, 255)

   
    window = pygame.display.set_mode((width,height))
    pygame.display.set_caption(f"{Titulo}")

    input = TextInputBox(width//2-150, height//2-40, 300, 40, PCBUTTON, SCBUTTON, "Enter music")
    iconEsc=pygame.image.load("./images/game/escIcon.png")
    iconEsc=pygame.transform.scale(iconEsc, (50,50))
    iconEscRect=iconEsc.get_rect()
    iconEscRect.topleft=(width//2+300,height//5-10)
    surfaceMusic=pygame.Surface((width/6,40))
    search_music_button=Button('buscar cancion',120,20,(width/3+300,height/14.4*3+80),5,SCBUTTON,FONTEdit)
    add_music_button=Button('Editar',50,20,(width/3+150,height/14.4*3+80),5,SCBUTTON,FONTEdit)
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
                screen(username)
            
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
                    print('resultado del update musica',updateFunct(id,newName,newArtist,newUrl,name,artist))

                elif iconEscRect.collidepoint(mouse_pos):
                    running=False
                    screen(username)
                
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
        window.blit(surfaceMusic, (width/7,height/14.4*10))
        if len(set_music)>0:
               
                add_music_button.draw(PCBUTTON,TCBUTTOM,window)
        window.blit(iconEsc,iconEscRect)
        pygame.display.flip()

    
    #Usuario.updateEmail(id, new_email)  # Update the email in the database
    pygame.quit()
